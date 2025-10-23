import mysql.connector 
import tkinter as tk
from tkinter import ttk, messagebox
import sys, os
    
def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="kiosco"
        )
        return conexion
    except mysql.connector.Error as err:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos:\n{err}")
        return None

class AgregarCategorias:

    def __init__(self, root):
        self.root = root
        self.root.title("Agregar Categoria- Kiosco")
        self.root.geometry("400x200")
        self.root.resizable(False, False)
       
        # Frame principal para ingresar categoría
        frame_ingresar_categoria = tk.LabelFrame(root, text="Ingresar Categoría", padx=10, pady=10)
        frame_ingresar_categoria.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        # Etiqueta y campo de entrada
        tk.Label(frame_ingresar_categoria, text="Nombre de la categoría:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.categoria_entry = tk.Entry(frame_ingresar_categoria, width=30)
        self.categoria_entry.grid(row=0, column=1, padx=5, pady=5)

        # Frame para los botones
        frame_botones = tk.LabelFrame(root)
        frame_botones.grid(row=1, column=0, sticky="e")

        # Botón para guardar categoría
        btn_guardar = tk.Button(frame_botones, text="Guardar Categoría", command=self.guardar_categoria, bg="#8A1B5A", fg="white")
        btn_guardar.grid(row=0, column=0, padx=5, pady=5)
        
    def guardar_categoria(self):
        
        nombre_categoria = self.categoria_entry.get()
    
        if not nombre_categoria:
            messagebox.showwarning("Campo vacío", "Por favor ingresá un nombre de categoría.")
            return

        try:
            conexion = conectar()
            cursor = conexion.cursor()
            query ="INSERT INTO categoria (nombre) VALUES (%s)"
            valores = [nombre_categoria]
            cursor.execute(query, valores)
            conexion.commit()
            conexion.close()
            messagebox.showinfo("Categoría guardada", f"Se guardó: {nombre_categoria}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la categoría:\n{e}")

    
if __name__ == "__main__":
    root = tk.Tk()
    app = AgregarCategorias(root)
    root.mainloop()
