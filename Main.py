import tkinter as tk
from Controller.Controller import SimuladorControlador

if __name__ == "__main__":
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Simulador de Procesos")

    # Configurar el tamaño de la ventana
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    min_width = int(screen_width * 0.4)
    min_height = int(screen_height * 0.8)
    root.geometry(f"{min_width}x{min_height}")
    root.minsize(min_width, min_height)

    # Inicializar el controlador
    app = SimuladorControlador(root)

    # Ejecutar el bucle principal de la aplicación
    root.mainloop()