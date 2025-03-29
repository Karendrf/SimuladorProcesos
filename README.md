# Simulador de Procesos

Este proyecto es un simulador de procesos. Permite simular la ejecución de procesos en los estados "Nuevo", "Listo", "Ejecucion", "Espera" y "Terminado" en diferentes algoritmos de gestión de memoria, como **Continua Fija**, **Continua Dinámica**, **Paginación** y **Segmentación**. Usa el algoritmo de planificacion First Come, First Served (FCFS)

---

## **Estructura del Proyecto**

El proyecto está dividido en tres componentes principales:

1. **Modelo (`Model`)**: Contiene la lógica de negocio y los datos del simulador.
2. **Vista (`View`)**: Maneja la interfaz gráfica de usuario (GUI).
3. **Controlador (`Controller`)**: Actúa como intermediario entre el modelo y la vista.

---

## **Clases y Métodos**

### **1. Modelo (`Model.py`)**

#### **Clase `Proceso`**
Representa un proceso en el simulador.

- **`__init__(self, pid, rafaga, memoria)`**: Constructor que inicializa un proceso con:
  - `pid`: Identificador único del proceso.
  - `rafaga`: Tiempo de ráfaga del proceso.
  - `memoria`: Cantidad de memoria requerida por el proceso.

#### **Clase `Contenedor`**
Representa un contenedor de memoria.

- **`__init__(self, numero, tamaño)`**: Constructor que inicializa un contenedor con:
  - `numero`: Identificador único del contenedor.
  - `tamaño`: Tamaño total del contenedor.

#### **Clase `SimuladorModelo`**
Contiene la lógica de negocio del simulador.

- **`__init__(self)`**: Inicializa las listas de procesos y contenedores.
- **`inicializar_procesos(self)`**: Crea una lista inicial de procesos con valores aleatorios.
- **`agregar_proceso(self)`**: Crea un nuevo proceso con valores aleatorios y lo agrega a la lista de procesos.
- **`liberar_contenedor(self, proceso)`**: Libera todos los contenedores asociados a un proceso.
- **`manejar_contenedores_dinamicos(self, proceso, algoritmo)`**: Asigna contenedores a un proceso según el algoritmo seleccionado.
  - **`_manejar_continua_dinamica(self, proceso)`**: Implementa la lógica para el algoritmo de **Continua Dinámica**.
  - **`_manejar_paginacion(self, proceso)`**: Implementa la lógica para el algoritmo de **Paginación**.
  - **`_manejar_segmentacion(self, proceso)`**: Implementa la lógica para el algoritmo de **Segmentación**.
  - **`_manejar_continua_fija(self, proceso)`**: Implementa la lógica para el algoritmo de **Continua Fija**.

---

### **2. Vista (`View.py`)**

#### **Clase `SimuladorVista`**
Maneja la interfaz gráfica de usuario (GUI).

- **`__init__(self, root)`**: Inicializa la ventana principal y los elementos de la interfaz, como tablas, botones y gráficos.
- **`configurar_diagrama(self)`**: Configura el grafo para el diagrama de estados.
- **`dibujar_diagrama(self, textos_secundarios)`**: Dibuja el diagrama de estados del sistema.
- **`actualizar_tabla_procesos(self, procesos)`**: Actualiza la tabla de procesos con los datos actuales.
- **`actualizar_tabla_contenedores(self, contenedores)`**: Actualiza la tabla de contenedores con los datos actuales.
- **`actualizar_tabla_logica(self, contenedores)`**: Actualiza la tabla de direcciones lógicas con los datos actuales.

---

### **3. Controlador (`Controller.py`)**

#### **Clase `SimuladorControlador`**
Actúa como intermediario entre el modelo y la vista.

- **`__init__(self, root)`**: Inicializa el modelo y la vista, y conecta los botones de la vista con los métodos del controlador.
- **`iniciar_simulacion(self)`**: Inicia o pausa la simulación.
- **`reiniciar_simulacion(self)`**: Reinicia la simulación al estado inicial.
- **`agregar_proceso(self)`**: Agrega un nuevo proceso al modelo y lo actualiza en la vista.
- **`mover_a_listo(self, proceso)`**: Mueve un proceso al estado "Listo".
- **`interrumpir_proceso(self)`**: Interrumpe el proceso en ejecución.
- **`ejecutar_proceso(self)`**: Inicia la ejecución de los procesos.
- **`pasar_a_listo(self)`**: Mueve los procesos del estado "Nuevo" al estado "Listo".
- **`ejecutar_revisiones(self)`**: Realiza revisiones periódicas durante la simulación.
- **`manejar_interrupcion(self)`**: Maneja la interrupción de un proceso.
- **`actualizar_vista(self)`**: Actualiza la vista con los datos del modelo.
- **`generar_array_procesos(self)`**: Genera un array con los estados de los procesos para el diagrama.

---

## **Flujo de la Simulación**

1. **Inicio de la simulación:**
   - Los procesos se inicializan en el estado "Nuevo".
   - Los procesos se mueven al estado "Listo" según el algoritmo seleccionado.

2. **Ejecución de procesos:**
   - Los procesos en estado "Listo" pasan a "Ejecución".
   - La ráfaga del proceso en ejecución disminuye en cada ciclo.

3. **Interrupciones:**
   - Un proceso en ejecución puede ser interrumpido y pasar al estado "Espera".

4. **Finalización:**
   - Cuando la ráfaga de un proceso llega a 0, pasa al estado "Terminado" y libera sus contenedores.

---

## **Algoritmos de Gestión de Memoria**

1. **Continua Fija:**
   - Los contenedores tienen un tamaño fijo de 40 unidades.
   - Solo los procesos con memoria ≤ 40 pueden ser asignados.
   - Los contenedores con memoria > 40 no podran ser asignados por lo que no pasaran a "Listo"
   - Los contenedores de memorias creados permanecen hasta el final de la ejecucion o su reinicio, y los porcesos buscaran por orden de contenedor uno disponible

2. **Continua Dinámica:**
   - Los contenedores se crean dinámicamente con el tamaño exacto necesario.
   - Los contenedores de memorias creados permanecen hasta el final de la ejecucion o su reinicio, y los porcesos buscaran por orden de contenedor un disponible

3. **Paginación:**
   - La memoria del proceso se divide en páginas de tamaño 10.
   - Los procesos se dividen en paginas de maximo 10 priorizando que cada division ocupe todo un contenedor
   - Cada página se asigna a un contenedor de tamaño 10.
   - Los contenedores de memorias creados permanecen hasta el final de la ejecucion o su reinicio, y los porcesos buscaran por orden de contenedor uno disponible

4. **Segmentación:**
   - La memoria del proceso se divide en segmentos de tamaño variable.
   - Los procesos se dividen aleatoriamente entre 3 a 6 segmentos para simular la division de partes del proceso
   - Las divisiones de los segmentos no son necesariamente del mismo tamaño
   - Cada segmento se asigna a un contenedor con suficiente espacio.
   - Los contenedores de memorias creados permanecen hasta el final de la ejecucion o su reinicio, y los porcesos buscaran por orden de contenedor uno disponible
