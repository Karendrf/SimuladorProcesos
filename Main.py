import tkinter as tk
import sys
from Controller.Controller import SimuladorControlador

if __name__ == "__main__":

    """
    Punto de entrada principal del programa. Configura la ventana principal,
    inicializa el controlador y ejecuta el bucle principal de la aplicación.
    """

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

    # Configurar el evento de cierre de la ventana
    # Inicializar el controlador
    app = SimuladorControlador(root)

    def cerrar_ventana():
        """
        Cierra la ventana principal y finaliza el programa

        Argumentos:
        No recibe argumentos

        Retorno:
        No retorna nada
        """  
        try:
            # Limpiar recursos del controlador
            if hasattr(app, 'cleanup'):
                app.cleanup()
            
            # Destruir la ventana
            root.quit()
            root.destroy()
        except Exception as e:
            print(f"Error al cerrar: {e}")
            sys.exit(1)

    root.protocol("WM_DELETE_WINDOW", cerrar_ventana)

    try:
        # Ejecutar el bucle principal de la aplicación
        root.mainloop()
        #Excepción incorporada que ocurre cuando el usuario interrumpe la ejecución de un programa utilizando
        #una acción de teclado, típicamente presionando Ctrl+C
    except KeyboardInterrupt:
        cerrar_ventana()

    