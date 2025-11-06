import mysql.connector 
import tkinter as tk
from tkinter import ttk, messagebox
import sys, os
import subprocess

def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="kiosco"
        )
        return conexion
    except mysql.connector.Error as err:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos:\n{err}")
        return None

class InventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventario - Kiosco")
        self.root.geometry("900x700")
        self.root.resizable(False, False)

       
        # Frame contenedor categoria y proveedores 
        frame_datos = tk.LabelFrame(root, text="Datos del producto", padx=10, pady=10)
        frame_datos.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        categorias_existentes = self.get_categorias()
        self.dict_categoria = {nombre: id_cat for id_cat, nombre in categorias_existentes}
        nombres_categorias = list(self.dict_categoria.keys())
        
        proveedores_existentes = self.get_proveedores()
        self.dict_proveedores = {nombre: id_prov for id_prov, nombre in proveedores_existentes}
        nombres_proveedores = list(self.dict_proveedores.keys())
        
        
        tk.Label(frame_datos, text="Categoria").grid(row=0,column=0, sticky="w")
        self.categoria_var = tk.StringVar()
        self.categoria_combo = ttk.Combobox(frame_datos, textvariable=self.categoria_var, values=nombres_categorias, width=28, state="readonly")
        self.categoria_combo.grid(row=0, column=1, padx=5, pady=2)
        tk.Button(frame_datos, text="Agregar Categoría", command=self.agregar_categoria, bg="#99F81D", fg="white").grid(row=0, column=2)
    
         # Nombre del producto
        tk.Label(frame_datos, text="Nombre del producto:").grid(row=1, column=0, sticky="w")
        self.nombre_entry = tk.Entry(frame_datos, width=30)
        self.nombre_entry.grid(row=1, column=1, padx=5, pady=2)

        # ID del producto
        tk.Label(frame_datos, text="Codigo de articulo:").grid(row=1, column=2, sticky="w")
        self.codigo_articulo_entry = tk.Entry(frame_datos, width=10)
        self.codigo_articulo_entry.grid(row=1, column=3, padx=5, pady=2)

        # Precio
        tk.Label(frame_datos, text="Precio:").grid(row=3, column=0, sticky="w")
        self.precio_entry = tk.Entry(frame_datos, width=30)
        self.precio_entry.grid(row=3, column=1, padx=5, pady=2)

        # Cantidad 
        tk.Label(frame_datos, text="Cantidad:").grid(row=4, column=0, sticky="w")
        self.cantidad_entry = tk.Entry(frame_datos, width=30)
        self.cantidad_entry.grid(row=4, column=1, padx=5, pady=2)

        tk.Label(frame_datos, text="Proveedor").grid(row=5,column=0, sticky="w")
        self.proveedor_var = tk.StringVar()
        self.proveedor_combo = ttk.Combobox(frame_datos, textvariable=self.proveedor_var, values=nombres_proveedores, width=28, state="readonly") 
        self.proveedor_combo.grid(row=5, column=1, padx=5, pady=2)
        #tk.Label(frame_datos, text="Proovedor:").grid(row=5, column=0, sticky="w")
        #self.proovedor_entry = tk.Entry(frame_datos, width=30)
        #self.proovedor_entry.grid


        # ---------- Botones ----------
        frame_botones = tk.LabelFrame(root, text="Botones", padx=10, pady=10)
        frame_botones.grid(row=0, column=1, padx=15, pady=10, sticky="ne") 

        # Botones en fila horizontal
        tk.Button(frame_botones, text="Agregar producto", command=self.agregar_producto, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5, pady=5)
        tk.Button(frame_botones, text="Actualizar lista", command=self.mostrar_productos, bg="#2196F3", fg="white").grid(row=1, column=0, padx=5, pady=5)
        tk.Button(frame_botones, text="Borrar Producto", command=self.borrar_producto, bg="#F70707", fg="white").grid(row=1, column=1, padx=5, pady=5)

        # ---------- Tabla ----------
        columnas = ("NOMBRE", "PRECIO", "COD ARTICULO", "CANTIDAD")
        self.tabla = ttk.Treeview(root, columns=columnas, show="headings")
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=100)
        self.tabla.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.mostrar_productos()

    # ---------- Función para agregar producto ----------
    def agregar_producto(self):
        nombre = self.nombre_entry.get()
        id_categoria = self.obtener_id_categoria()
        precio = self.precio_entry.get()
        codigo_articulo = self.codigo_articulo_entry.get()
        cantidad = self.cantidad_entry.get()
        #stock = self.stock_entry.get()
        #id_proveedor = self.proovedor_entry.get()

        if not nombre or not precio:
            messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos obligatorios.")
            return

        try:
            conexion = conectar()
            cursor = conexion.cursor()
            query = "INSERT INTO producto (nombre, id_categoria, codigo_articulo, precio, cantidad) VALUES (%s, %s, %s, %s,%s)" #saque stock y id_proveedor por que son tablas aparte 
            valores = (nombre, id_categoria, codigo_articulo, float(precio), cantidad)
            cursor.execute(query, valores)
            conexion.commit()
            conexion.close()

            messagebox.showinfo("Éxito", "Producto agregado correctamente.")
            self.mostrar_productos()
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el producto.\n{e}")

    def obtener_id_categoria(self):
        nombre = self.categoria_var.get()
        return self.dict_categoria.get(nombre) 
    
    def agregar_categoria(self):
        ruta = os.path.join(os.path.dirname(__file__), "agregar_categoria.py")
        try:
            subprocess.Popen(["python", ruta])
        except Exception as e:
         messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")

    def get_categorias(self):
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_categoria, nombre FROM categoria")
        categorias = cursor.fetchall()  # Devuelve lista de tuplas [(1, "Gaseosas"), (2, "Snacks"), ...]
        conexion.close()
        return categorias
    
    def get_proveedores(self):
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_proveedor, nombre FROM proveedor")
        proveedores = cursor.fetchall()  # Devuelve lista de tuplas [(1, "Gaseosas"), (2, "Snacks"), ...]
        conexion.close()
        return proveedores
    

    def borrar_producto (self):
        nombre = self.nombre_entry.get()

    
    
    def mostrar_productos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre, precio, codigo_articulo, cantidad FROM kiosco.producto;")
        for fila in cursor.fetchall():
            self.tabla.insert("", "end", values=fila)
        conexion.close()


    def limpiar_campos(self):
        self.nombre_entry.delete(0, tk.END)
        #self.categoria_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)
        self.cantidad_entry.delete(0, tk.END)
    
    # ---------- 🔍 Función global: buscar producto por código ----------
def buscar_producto_por_codigo(codigo_articulo):
    """Devuelve un diccionario con los datos del producto según su código, o None si no existe."""
    try:
        conexion = conectar()
        if not conexion:
            return None

        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT id_producto, nombre, precio, cantidad, codigo_articulo FROM producto WHERE codigo_articulo = %s",
            (codigo_articulo,)
        )
        producto = cursor.fetchone()
        conexion.close()
        return producto
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo buscar el producto:\n{err}")
        return None



if __name__ == "__main__":
    root = tk.Tk()
    app = InventarioApp(root)
    root.mainloop()