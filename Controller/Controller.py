from Model.Model import SimuladorModelo
from View.View import SimuladorVista


class SimuladorControlador:
    """
    Controlador principal que conecta el modelo y la vista.
    """

    def __init__(self, root):
        """
        Inicializa el controlador, el modelo y la vista.

        Argumentos:
        root (tk.Tk): La ventana principal de la aplicación.

        Retorno:
        No retorna nada.
        """
        # Inicializar el modelo y la vista
        self.modelo = SimuladorModelo()
        self.vista = SimuladorVista(root)

        # Conectar botones de la vista a los métodos del controlador
        self.vista.btn_iniciar.config(command=self.iniciar_simulacion)
        self.vista.btn_reiniciar.config(command=self.reiniciar_simulacion)
        self.vista.btn_agregar.config(command=self.agregar_proceso)
        self.vista.btn_interrumpir.config(command=self.interrumpir_proceso)

        # Variables de control
        self.simulacion_en_curso = False
        self.simulacion_pausada = False
        self.temporizadores = []
        self.interrupcion = False

        # Inicializar procesos y actualizar la vista
        self.modelo.inicializar_procesos()
        self.actualizar_vista()

    def iniciar_simulacion(self):
        """
        Inicia, pausa o reanuda la simulación según el estado actual.

        Argumentos:
        No recibe argumentos.

        Retorno:
        No retorna nada.
        """
        if not self.simulacion_en_curso:
            # Iniciar la simulación
            self.simulacion_en_curso = True
            self.simulacion_pausada = False
            self.vista.btn_iniciar.config(text="Pausar Simulación")
            self.vista.combobox.config(state="disabled")
            self.ejecutar_proceso()
        elif not self.simulacion_pausada:
            # Pausar la simulación
            self.simulacion_pausada = True
            self.vista.btn_iniciar.config(text="Reanudar Simulación")
            for temporizador in self.temporizadores:
                self.vista.root.after_cancel(temporizador)
            self.temporizadores.clear()
        else:
            # Reanudar la simulación
            self.simulacion_pausada = False
            self.vista.btn_iniciar.config(text="Pausar Simulación")
            self.ejecutar_revisiones()

    def reiniciar_simulacion(self):
        """
        Reinicia la simulación, limpiando todos los procesos y contenedores.

        Argumentos:
        No recibe argumentos.

        Retorno:
        No retorna nada.
        """
        for temporizador in self.temporizadores:
            self.vista.root.after_cancel(temporizador)
        self.temporizadores.clear()
        self.modelo.procesos = []
        self.modelo.contenedorDinamico = []
        self.simulacion_en_curso = False
        self.simulacion_pausada = False
        self.interrupcion = False
        self.vista.btn_iniciar.config(text="Iniciar Simulación")
        self.vista.combobox.config(state="readonly")
        self.modelo.inicializar_procesos()
        self.actualizar_vista()

    def agregar_proceso(self):
        """
        Agrega un nuevo proceso al modelo y actualiza la vista.

        Argumentos:
        No recibe argumentos.

        Retorno:
        No retorna nada.
        """
        nuevo_proceso = self.modelo.agregar_proceso()
        self.actualizar_vista()

        # Si la simulación está en curso y no está pausada, mover el proceso a "Listo"
        if self.simulacion_en_curso and not self.simulacion_pausada:
            self.vista.root.after(500, lambda: self.mover_a_listo(nuevo_proceso))

    def mover_a_listo(self, proceso):
        """
        Mueve un proceso al estado "Listo" si cumple con los requisitos.

        Argumentos:
        proceso (Proceso): El proceso a mover al estado "Listo".

        Retorno:
        No retorna nada.
        """
        if self.simulacion_pausada:
            return

        algoritmo = self.vista.combobox.get()
        if algoritmo == "Continuia Fija" and proceso.memoria > 40:
            return
        else:
            proceso.estado = "Listo"
            self.modelo.manejar_contenedores_dinamicos(proceso, algoritmo)
            self.actualizar_vista()

    def interrumpir_proceso(self):
        """
        Marca una interrupción en la simulación.

        Argumentos:
        No recibe argumentos.

        Retorno:
        No retorna nada.
        """
        self.interrupcion = True

    def ejecutar_proceso(self):
        """
        Inicia la ejecución de los procesos en el modelo.

        Argumentos:
        No recibe argumentos.

        Retorno:
        No retorna nada.
        """
        for proceso in self.modelo.procesos:
            proceso.estado = "Nuevo"
        self.actualizar_vista()
        temporizador = self.vista.root.after(500, self.pasar_a_listo)
        self.temporizadores.append(temporizador)

    def pasar_a_listo(self):
        """
        Mueve los procesos en estado "Nuevo" al estado "Listo".

        Argumentos:
        No recibe argumentos.

        Retorno:
        No retorna nada.
        """
        for proceso in self.modelo.procesos:
            if proceso.estado == "Nuevo":
                algoritmo = self.vista.combobox.get()
                if algoritmo == "Continuia Fija" and proceso.memoria > 40:
                    continue
                else:
                    proceso.estado = "Listo"
                    self.modelo.manejar_contenedores_dinamicos(proceso, algoritmo)

        self.actualizar_vista()
        temporizador = self.vista.root.after(500, self.ejecutar_revisiones)
        self.temporizadores.append(temporizador)

    def ejecutar_revisiones(self):
        """
        Realiza revisiones periódicas durante la simulación para ver que cambios
        de estados en los procesos toca controlar.

        Argumentos:
        No recibe argumentos.

        Retorno:
        No retorna nada.
        """
        #Realiza revisiones periódicas durante la simulación.
        if self.simulacion_pausada:
            return
    
        # Si no hay proceso en ejecución, tomar el primer "Listo"
        proceso_ejecucion = next((p for p in self.modelo.procesos if p.estado == "Ejecución"), None)
        if not proceso_ejecucion:
            proceso_listo = next((p for p in self.modelo.procesos if p.estado == "Listo"), None)
            if proceso_listo:
                proceso_listo.estado = "Ejecución"
    
        # Si hay un proceso en "Espera", moverlo a "Listo" y colocarlo al final de la lista
        proceso_espera = next((p for p in self.modelo.procesos if p.estado == "Espera"), None)
        if proceso_espera:
            proceso_espera.estado = "Listo"
            self.modelo.procesos.remove(proceso_espera)  # Eliminar el proceso de su posición actual
            self.modelo.procesos.append(proceso_espera)  # Agregarlo al final de la lista
    
        # Mover procesos en estado "Nuevo" a "Listo"
        for proceso in self.modelo.procesos:
            if proceso.estado == "Nuevo":
                algoritmo = self.vista.combobox.get()
                if algoritmo == "Continuia Fija" and proceso.memoria > 40:
                    continue
                else:
                    proceso.estado = "Listo"
                    self.modelo.manejar_contenedores_dinamicos(proceso, algoritmo)
    
        # Si hay una interrupción, manejarla
        if self.interrupcion:
            self.manejar_interrupcion()
    
        # Resta 1 a la ráfaga del proceso en ejecución
        proceso_ejecucion = next((p for p in self.modelo.procesos if p.estado == "Ejecución"), None)
        if proceso_ejecucion:
            proceso_ejecucion.rafaga -= 1
            if proceso_ejecucion.rafaga <= 0:
                proceso_ejecucion.estado = "Terminado"
                self.modelo.liberar_contenedor(proceso_ejecucion)
    
        self.actualizar_vista()
    
        # Programar la siguiente revisión
        if not self.simulacion_pausada:
            temporizador = self.vista.root.after(1000, self.ejecutar_revisiones)
            self.temporizadores.append(temporizador)
            
    def manejar_interrupcion(self):
        """
        Controla el que hacer cuando existe una interrupción en la simulación.

        Argumentos:
        No recibe argumentos.

        Retorno:
        No retorna nada.
        """
        proceso_ejecucion = next((p for p in self.modelo.procesos if p.estado == "Ejecución"), None)
        if proceso_ejecucion:
            proceso_ejecucion.estado = "Espera"
            proceso_listo = next((p for p in self.modelo.procesos if p.estado == "Listo"), None)
            if proceso_listo:
                proceso_listo.estado = "Ejecución"
        self.interrupcion = False

    def actualizar_vista(self):
        """
        Actualiza la vista con los datos actuales del modelo.

        Argumentos:
        No recibe argumentos.

        Retorno:
        No retorna nada.
        """
        self.vista.actualizar_tabla_procesos(self.modelo.procesos)
        self.vista.actualizar_tabla_contenedores(self.modelo.contenedorDinamico)
        self.vista.actualizar_tabla_logica(self.modelo.contenedorDinamico)  # Llamar al método para actualizar la tabla lógica
        textos_secundarios = self.generar_array_procesos()
        self.vista.dibujar_diagrama(textos_secundarios)

    def generar_array_procesos(self):
        """
        Genera un array con los estados de los procesos para dibujarlos en 
        el diagrama.

        Argumentos:
        No recibe argumentos.

        Retorno:
        list: Lista de cadenas con los estados de los procesos.
        """
        #Genera un array con los estados de los procesos para el diagrama.
        estados_procesos = {"Nuevo": [], "Listo": [], "Ejecución": [], "Espera": [], "Terminado": []}
        for proceso in self.modelo.procesos:
            estados_procesos[proceso.estado].append(f"P{proceso.pid}")

        array_resultado = []
        for estado in ["Nuevo", "Listo", "Ejecución", "Espera", "Terminado"]:
            if estados_procesos[estado]:
                procesos_estado = estados_procesos[estado]
                string_estado = "\n".join(
                    [", ".join(procesos_estado[i:i + 3]) for i in range(0, len(procesos_estado), 3)]
                )
                array_resultado.append(string_estado)
            else:
                array_resultado.append(" ")
        return array_resultado