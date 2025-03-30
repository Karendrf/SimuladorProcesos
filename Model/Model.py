import random

class Proceso:
    """
    Clase que representa el objeto Proceso en el simulador.
    Contiene atributos para el identificador del proceso, tiempo de ráfaga,

    Argumentos:
    pid (int): Identificador único del proceso.
    rafaga (int): Tiempo de ráfaga del proceso.
    memoria (int): Cantidad de memoria requerida por el proceso.

    Retorno:
    No retorna nada.
    """
    def __init__(self, pid, rafaga, memoria):
        self.pid = pid
        self.rafaga = rafaga
        self.memoria = memoria
        self.estado = "Nuevo"
        self.tiempo_restante = rafaga


class Contenedor:
    """
    Representa un contenedor de memoria en el sistema.

    Argumentos:
    numero (int): Identificador único del contenedor.
    tamaño (int): Tamaño total del contenedor.

    Retorno:
    No retorna nada.
    """
    def __init__(self, numero, tamaño):
        self.numero = numero
        self.tamaño = tamaño
        self.proceso = None
        self.tamaño_ocupado = 0
        self.tamaño_restante = tamaño


class SimuladorModelo:
    """
    Modelo principal del simulador que gestiona procesos y contenedores.
    """

    def __init__(self):
        """
        Inicializa el modelo con listas vacías de procesos y contenedores.

        Argumentos:
        No recibe argumentos.

        Retorno:
        No retorna nada.
        """
        self.procesos = []
        self.contenedorDinamico = []

    def inicializar_procesos(self):
        """
        Inicializa una lista de procesos con valores aleatorios.

        Argumentos:
        No recibe argumentos.

        Retorno:
        No retorna nada.
        """
        #Inicializa una lista de procesos con valores aleatorios.
        self.procesos = [Proceso(i, random.randint(5, 10), random.randint(10, 50)) for i in range(3)]

    def agregar_proceso(self):
        """
        Crea un nuevo proceso con valores aleatorios y lo agrega a la lista de procesos.

        Argumentos:
        No recibe argumentos.

        Retorno:
        Proceso: El nuevo proceso creado.
        """     
        #Crea un nuevo proceso con valores aleatorios y lo agrega a la lista de procesos.
        nuevo_proceso = Proceso(len(self.procesos), random.randint(5, 10), random.randint(10, 50))
        self.procesos.append(nuevo_proceso)
        return nuevo_proceso

    def liberar_contenedor(self, proceso):
        """
        Libera todos los contenedores asociados a un proceso.

        Argumentos:
        proceso (Proceso): El proceso cuyos contenedores serán liberados.

        Retorno:
        No retorna nada.
        """
        #Libera todos los contenedores asociados a un proceso.
        for contenedor in self.contenedorDinamico:
            if contenedor.proceso == proceso:
                contenedor.proceso = None
                contenedor.tamaño_ocupado = 0
                contenedor.tamaño_restante = contenedor.tamaño

    def manejar_contenedores_dinamicos(self, proceso, algoritmo):
        """
        Asigna contenedores a un proceso según el algoritmo seleccionado.

        Argumentos:
        proceso (Proceso): El proceso al que se asignarán los contenedores.
        algoritmo (str): El algoritmo de asignación a utilizar.

        Retorno:
        No retorna nada.
        """
        #Asigna contenedores a un proceso según el algoritmo seleccionado.
        if algoritmo == "Continua Dinamica":
            self._manejar_continua_dinamica(proceso)
        elif algoritmo == "Paginacion":
            self._manejar_paginacion(proceso)
        elif algoritmo == "Segmentacion":
            self._manejar_segmentacion(proceso)
        elif algoritmo == "Continuia Fija":
            self._manejar_continua_fija(proceso)

    def _manejar_continua_dinamica(self, proceso):
        """
        Asigna contenedores dinámicos a un proceso.

        Argumentos:
        proceso (Proceso): El proceso al que se asignarán los contenedores.

        Retorno:
        No retorna nada.
        """
        for contenedor in self.contenedorDinamico:
            if contenedor.proceso == proceso:
                return

        contenedor_asignado = None
        for contenedor in self.contenedorDinamico:
            if contenedor.tamaño >= proceso.memoria and contenedor.proceso is None:
                contenedor.proceso = proceso
                contenedor.tamaño_ocupado = proceso.memoria
                contenedor.tamaño_restante = contenedor.tamaño - proceso.memoria
                contenedor_asignado = contenedor
                break

        if not contenedor_asignado:
            nuevo_contenedor = Contenedor(len(self.contenedorDinamico) + 1, proceso.memoria)
            nuevo_contenedor.proceso = proceso
            nuevo_contenedor.tamaño_ocupado = proceso.memoria
            nuevo_contenedor.tamaño_restante = nuevo_contenedor.tamaño - proceso.memoria
            self.contenedorDinamico.append(nuevo_contenedor)

    def _manejar_paginacion(self, proceso):
        """
        Asigna contenedores al proceso utilizando el algoritmo de paginación.

        Argumentos:
        proceso (Proceso): El proceso al que se asignarán los contenedores.

        Retorno:
        No retorna nada.
        """
        # Dividir la memoria del proceso en páginas de tamaño 10
        paginas = [10] * (proceso.memoria // 10)
        if proceso.memoria % 10 != 0:
            paginas.append(proceso.memoria % 10)
    
        for pagina in paginas:
            contenedor_asignado = None
            # Buscar un contenedor disponible
            for contenedor in self.contenedorDinamico:
                if contenedor.proceso is None and contenedor.tamaño == 10:
                    contenedor.proceso = proceso
                    contenedor.tamaño_ocupado = pagina
                    contenedor.tamaño_restante = contenedor.tamaño - pagina
                    contenedor_asignado = contenedor
                    break
    
            # Si no hay un contenedor disponible, crear uno nuevo de tamaño 10
            if not contenedor_asignado:
                nuevo_contenedor = Contenedor(len(self.contenedorDinamico) + 1, 10)
                nuevo_contenedor.proceso = proceso
                nuevo_contenedor.tamaño_ocupado = pagina
                nuevo_contenedor.tamaño_restante = nuevo_contenedor.tamaño - pagina
                self.contenedorDinamico.append(nuevo_contenedor)

    def _manejar_segmentacion(self, proceso):
        """
        Asigna contenedores al proceso utilizando el algoritmo de segmentación.

        Argumentos:
        proceso (Proceso): El proceso al que se asignarán los contenedores.

        Retorno:
        No retorna nada.
        """
        segmentos_asignados = sum(
            contenedor.tamaño_ocupado for contenedor in self.contenedorDinamico if contenedor.proceso == proceso
        )
        if segmentos_asignados >= proceso.memoria:
            return
        #Generar segmentos aleatorios para el proceso
        num_segmentos = random.randint(3, 6)
        segmentos = []
        memoria_restante = proceso.memoria

        for i in range(num_segmentos):
            if i == num_segmentos - 1:
                segmentos.append(memoria_restante)
            else:
                max_segmento = memoria_restante // (num_segmentos - i) + random.randint(-2, 2)
                max_segmento = max(1, min(max_segmento, memoria_restante))
                segmentos.append(max_segmento)
                memoria_restante -= max_segmento

        for segmento in segmentos:
            contenedor_asignado = None
            for contenedor in self.contenedorDinamico:
                if contenedor.proceso is None and contenedor.tamaño >= segmento:
                    contenedor.proceso = proceso
                    contenedor.tamaño_ocupado = segmento
                    contenedor.tamaño_restante = contenedor.tamaño - segmento
                    contenedor_asignado = contenedor
                    break

            if not contenedor_asignado:
                nuevo_contenedor = Contenedor(len(self.contenedorDinamico) + 1, segmento)
                nuevo_contenedor.proceso = proceso
                nuevo_contenedor.tamaño_ocupado = segmento
                nuevo_contenedor.tamaño_restante = nuevo_contenedor.tamaño - segmento
                self.contenedorDinamico.append(nuevo_contenedor)

    def _manejar_continua_fija(self, proceso):
        """
        Asigna contenedores al proceso utilizando el algoritmo de memoria continua fija.

        Argumentos:
        proceso (Proceso): El proceso al que se asignarán los contenedores.

        Retorno:
        No retorna nada.
        """
        for contenedor in self.contenedorDinamico:
            if contenedor.proceso == proceso:
                return

        contenedor_asignado = None
        for contenedor in self.contenedorDinamico:
            if contenedor.tamaño == 40 and contenedor.proceso is None:
                contenedor.proceso = proceso
                contenedor.tamaño_ocupado = proceso.memoria
                contenedor.tamaño_restante = contenedor.tamaño - proceso.memoria
                contenedor_asignado = contenedor
                break

        if not contenedor_asignado:
            nuevo_contenedor = Contenedor(len(self.contenedorDinamico) + 1, 40)
            nuevo_contenedor.proceso = proceso
            nuevo_contenedor.tamaño_ocupado = proceso.memoria
            nuevo_contenedor.tamaño_restante = nuevo_contenedor.tamaño - proceso.memoria
            self.contenedorDinamico.append(nuevo_contenedor)