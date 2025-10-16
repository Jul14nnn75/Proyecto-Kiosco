import tkinter as tk
from tkinter import Menu
import subprocess
import sys
import os

def abrir_punto_de_venta():
    """
    Abre la ventana principal del sistema (antes main.py, ahora ventana.py)
    """
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ventana_path = os.path.join(ruta_actual, "ventana.py")

    # Ejecuta ventana.py como un nuevo proceso de Python
    subprocess.Popen([sys.executable, ventana_path])

# --- Ventana principal del sistema ---
root = tk.Tk()
root.title("Sistema de Kiosco")
root.geometry("600x400")
root.configure(bg="white")

# Crear barra de menú
menubar = Menu(root)

# Menú de Venta
menu_venta = Menu(menubar, tearoff=0)
menu_venta.add_command(label="Punto de venta", command=abrir_punto_de_venta)
menubar.add_cascade(label="Venta", menu=menu_venta)

# Asignar la barra de menú a la ventana principal
root.config(menu=menubar)

# Etiqueta de bienvenida
label = tk.Label(root, text="Bienvenido al Sistema de Kiosco", bg="white", font=("Arial", 16))
label.pack(pady=150)

# Iniciar loop principal
root.mainloop()
