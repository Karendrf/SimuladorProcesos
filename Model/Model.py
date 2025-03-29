import random

class Proceso:
    def __init__(self, pid, rafaga, memoria):
        self.pid = pid
        self.rafaga = rafaga
        self.memoria = memoria
        self.estado = "Nuevo"
        self.tiempo_restante = rafaga


class Contenedor:
    def __init__(self, numero, tamaño):
        self.numero = numero
        self.tamaño = tamaño
        self.proceso = None
        self.tamaño_ocupado = 0
        self.tamaño_restante = tamaño


class SimuladorModelo:
    def __init__(self):
        self.procesos = []
        self.contenedorDinamico = []

    def inicializar_procesos(self):
        #Inicializa una lista de procesos con valores aleatorios.
        self.procesos = [Proceso(i, random.randint(5, 10), random.randint(10, 50)) for i in range(3)]

    def agregar_proceso(self):
        #Crea un nuevo proceso con valores aleatorios y lo agrega a la lista de procesos.
        nuevo_proceso = Proceso(len(self.procesos), random.randint(5, 10), random.randint(10, 50))
        self.procesos.append(nuevo_proceso)
        return nuevo_proceso

    def liberar_contenedor(self, proceso):
        #Libera todos los contenedores asociados a un proceso.
        for contenedor in self.contenedorDinamico:
            if contenedor.proceso == proceso:
                contenedor.proceso = None
                contenedor.tamaño_ocupado = 0
                contenedor.tamaño_restante = contenedor.tamaño

    def manejar_contenedores_dinamicos(self, proceso, algoritmo):
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