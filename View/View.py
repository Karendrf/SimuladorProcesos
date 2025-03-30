import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx


class SimuladorVista:
    def __init__(self, root):
        """
        Crea la ventana principal, sus componentes y los ubica sobre la hoja (root).

        Argumentos:
        root (tk.Tk): La ventana principal de la aplicación.

        Retorno:
        No retorna nada.
        """
        self.root = root
        self.root.title("Simulador de Procesos")
        self.temporizadores = []

        # Etiqueta de título
        self.titulo = tk.Label(root, text="Simulación de Procesos", font=("Arial", 14))
        self.titulo.place(relx=0.1, rely=0.01, relwidth=0.8, relheight=0.05)

        # Crear la tabla de procesos
        self.tree = ttk.Treeview(root, columns=("PID", "Estado", "Ráfaga", "Memoria"), show='headings')
        for col in ("PID", "Estado", "Ráfaga", "Memoria"):
            self.tree.heading(col, text=col)

        self.tree.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.4)
        self.root.update_idletasks()
        table_width = self.tree.winfo_width()
        column_width = int(table_width / 4)

        self.tree.column("PID", width=column_width, anchor="center")
        self.tree.column("Estado", width=column_width, anchor="center")
        self.tree.column("Ráfaga", width=column_width, anchor="center")
        self.tree.column("Memoria", width=column_width, anchor="center")

        self.tree.place(relx=0.03, rely=0.06, relwidth=0.5, relheight=0.25)

        # Botones
        self.btn_iniciar = tk.Button(root, text="Iniciar Simulación")
        self.btn_iniciar.place(relx=0.55, rely=0.08, relwidth=0.2, relheight=0.05)

        self.btn_reiniciar = tk.Button(root, text="Reiniciar Simulación")
        self.btn_reiniciar.place(relx=0.77, rely=0.08, relwidth=0.2, relheight=0.05)

        self.btn_agregar = tk.Button(root, text="Agregar Proceso")
        self.btn_agregar.place(relx=0.55, rely=0.15, relwidth=0.2, relheight=0.05)

        self.btn_interrumpir = tk.Button(root, text="Interrumpir Proceso")
        self.btn_interrumpir.place(relx=0.77, rely=0.15, relwidth=0.2, relheight=0.05)

        # Combobox para seleccionar el tipo de algoritmo
        self.combolabel = tk.Label(root, text="Seleccionar Algoritmo de memoria:", font=("Arial", 9, "bold"))
        self.combolabel.place(relx=0.55, rely=0.21, relwidth=0.4, relheight=0.05)

        valores = ["Continuia Fija", "Continua Dinamica", "Paginacion", "Segmentacion"]
        self.combobox = ttk.Combobox(root, values=valores, state="readonly")
        self.combobox.set(valores[1])
        self.combobox.place(relx=0.55, rely=0.26, relwidth=0.4, relheight=0.05)

        # Gráfico
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().place(relx=0.05, rely=0.33, relwidth=0.9, relheight=0.35)

        # Etiquetas para tablas de memoria y lógica
        self.titulo_memoria = tk.Label(root, text="Tabla de asignación de memoria", font=("Arial", 10, "bold"))
        self.titulo_memoria.place(relx=0.05, rely=0.7, relwidth=0.55, relheight=0.05)

        self.titulo_logica = tk.Label(root, text="Tabla de direcciones", font=("Arial", 10, "bold"))
        self.titulo_logica.place(relx=0.61, rely=0.7, relwidth=0.35, relheight=0.05)

        # Crear la tabla de contenedores
        self.tree_contenedores = ttk.Treeview(root, columns=("N°", "Tamaño", "Proceso", "Ocupado", "Restante"), show='headings')
        for col in ("N°", "Tamaño", "Proceso", "Ocupado", "Restante"):
            self.tree_contenedores.heading(col, text=col)

        self.root.update_idletasks()
        table_width = self.tree_contenedores.winfo_width()
        column_width = int(table_width / 5)

        self.tree_contenedores.column("N°", width=column_width, anchor="center")
        self.tree_contenedores.column("Tamaño", width=column_width, anchor="center")
        self.tree_contenedores.column("Proceso", width=column_width, anchor="center")
        self.tree_contenedores.column("Ocupado", width=column_width, anchor="center")
        self.tree_contenedores.column("Restante", width=column_width, anchor="center")
        self.tree_contenedores.place(relx=0.05, rely=0.75, relwidth=0.55, relheight=0.23)

        # Crear la tabla lógica
        self.tree_logica = ttk.Treeview(root, columns=("Proceso", "Contenedores"), show='headings')
        self.tree_logica.heading("Proceso", text="Proceso")
        self.tree_logica.heading("Contenedores", text="Contenedores")

        self.root.update_idletasks()
        table_width = self.tree_logica.winfo_width()
        self.tree_logica.column("Proceso", width=int(table_width * 0.3), anchor="center")
        self.tree_logica.column("Contenedores", width=int(table_width * 0.7), anchor="center")
        self.tree_logica.place(relx=0.61, rely=0.75, relwidth=0.35, relheight=0.23)

        # Configurar el grafo
        self.grafo = nx.DiGraph()
        self.configurar_diagrama()

    def configurar_diagrama(self):  
        """
        Configura el grafo para el diagrama de estados.

        Argumentos:
        no recibe argumentos

        Retorno:
        No retorna nada.
        """
        self.grafo.add_edges_from([
            ("Nuevo", "Listo"), ("Listo", "Ejecución"), ("Ejecución", "Espera"),
            ("Ejecución", "Terminado"), ("Espera", "Listo")
        ])
        self.pos = {
            "Nuevo": (0, 2), "Listo": (2, 2), "Ejecución": (4, 2),
            "Espera": (4, 0.5), "Terminado": (6, 2)
        }

    def dibujar_diagrama(self, textos_secundarios):
        """
        Dibuja el diagrama de estados del sistema.

        Argumentos:
        textos_secundarios (list): Lista de textos secundarios (Procesos en cada nodo).

        Retorno:
        No retorna nada.
        """
        self.ax.clear()
        colores_nodos = {
            "Nuevo": "lightgray",
            "Listo": "lightcoral",
            "Ejecución": "lightgreen",
            "Espera": "lightblue",
            "Terminado": "lightpink"
        }
        colores = [colores_nodos[nodo] for nodo in self.grafo.nodes()]
        nx.draw(
            self.grafo, self.pos, with_labels=False, node_color=colores,
            edge_color="black", node_size=2000, font_size=10, font_weight="bold", ax=self.ax
        )
        pos_labels = {nodo: (x, y + 0.8) for nodo, (x, y) in self.pos.items()}
        etiquetas = {
            "Nuevo": "Nuevo",
            "Listo": "Listo",
            "Ejecución": "Ejecución",
            "Espera": "Espera",
            "Terminado": "Terminado"
        }
        for nodo, (x, y) in pos_labels.items():
            texto = etiquetas[nodo]
            color_etiqueta = colores_nodos[nodo]
            self.ax.text(
                x, y, texto, fontsize=8, fontweight="bold", ha="center", va="center", color="black",
                bbox=dict(facecolor=color_etiqueta, edgecolor="black", boxstyle="round,pad=0.3")
            )
        for i, (nodo, (x, y)) in enumerate(self.pos.items()):
            texto_secundario = textos_secundarios[i] if i < len(textos_secundarios) else ""
            self.ax.text(
                x, y, texto_secundario, fontsize=6, fontweight="normal", ha="center", va="center",
                color="black"
            )
        self.ax.set_xlim(-1, 7)
        self.ax.set_ylim(0, 3)
        self.canvas.draw()

    def actualizar_tabla_procesos(self, procesos):
        """
        Actualiza la tabla de procesos con los datos actuales.

        Argumentos:
        procesos (list): Lista de procesos a mostrar en la tabla.

        Retorno:
        No retorna nada.
        """
        #Actualiza la tabla de procesos con los datos actuales.
        self.tree.tag_configure("Nuevo", foreground="dimgray")
        self.tree.tag_configure("Listo", foreground="darkred")
        self.tree.tag_configure("Ejecución", foreground="darkgreen")
        self.tree.tag_configure("Espera", foreground="darkblue")
        self.tree.tag_configure("Terminado", foreground="darkmagenta")
    
        for row in self.tree.get_children():
            self.tree.delete(row)
    
        for proceso in procesos:
            self.tree.insert(
                "", "end",
                values=(proceso.pid, proceso.estado, proceso.rafaga, proceso.memoria),
                tags=(proceso.estado,)
            )

    def actualizar_tabla_contenedores(self, contenedores):
        """
        Actualiza la tabla de contenedores con los datos actuales.

        Argumentos:
        contenedores (list): Lista de contenedores a mostrar en la tabla.

        Retorno:
        No retorna nada.
        """
        #Actualiza la tabla de contenedores con los datos actuales
        for row in self.tree_contenedores.get_children():
            self.tree_contenedores.delete(row)

        for contenedor in contenedores:
            proceso_asignado = f"P{contenedor.proceso.pid}" if contenedor.proceso else "Ninguno"
            self.tree_contenedores.insert(
                "", "end",
                values=(contenedor.numero, contenedor.tamaño, proceso_asignado, contenedor.tamaño_ocupado, contenedor.tamaño_restante)
            )

    def actualizar_tabla_logica(self, contenedores):
        """
        Actualiza la tabla de direcciones con los datos actuales.

        Argumentos:
        contenedores (list): Lista de contenedores a mostrar en la tabla lógica.

        Retorno:
        No retorna nada.
        """
        #Actualiza la tabla de direcciones con los datos actuales
        for row in self.tree_logica.get_children():
            self.tree_logica.delete(row)
    
        # Agrupar los contenedores por proceso
        procesos_contenedores = {}
        for contenedor in contenedores:
            if contenedor.proceso:
                proceso_id = f"P{contenedor.proceso.pid}"
                if proceso_id not in procesos_contenedores:
                    procesos_contenedores[proceso_id] = []
                procesos_contenedores[proceso_id].append(f"C{contenedor.numero}")
    
        for proceso, contenedores in procesos_contenedores.items():
            self.tree_logica.insert("", "end", values=(proceso, ",".join(contenedores)))