import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_APP = os.path.join(BASE_DIR, "main_app.py")
GESTION_TURNOS = os.path.join(BASE_DIR, "turno3.py")

# ----------------- CONFIGURACIÓN DE CONEXIÓN -----------------
def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # ← coloca tu contraseña de MySQL si tiene
            database="kiosco"
        )
        return conexion
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos:\n{err}")
        return None

# ----------------- FUNCIÓN LOGIN -----------------
def iniciar_sesion():
    nombre = entry_usuario.get()
    password = entry_contraseña.get()

    if not nombre or not password:
        messagebox.showwarning("Advertencia", "Debe completar todos los campos")
        return

    conexion = conectar_bd()
    if conexion is None:
        return
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuario WHERE nombre=%s AND contraseña=%s", (nombre, password))
    usuario = cursor.fetchone()

    if usuario:
        tipo = usuario["tipo"].lower()
        messagebox.showinfo("Bienvenido", f"Inicio de sesión exitoso como {tipo.capitalize()}")
    ventana.destroy()
    if tipo == "admin":
        # Admin entra directo al sistema principal
        subprocess.Popen([sys.executable, MAIN_APP], cwd=BASE_DIR)
    elif tipo == "empleado":
        # Empleado primero pasa por gestión de turnos
        subprocess.run([sys.executable, GESTION_TURNOS], cwd=BASE_DIR)
        subprocess.Popen([sys.executable, MAIN_APP], cwd=BASE_DIR)
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    cursor.close()
    conexion.close()

# ----------------- FUNCIÓN CREAR USUARIO -----------------
def crear_usuario():
    def guardar_usuario():
        nombre = entry_nombre_nuevo.get()
        password = entry_contraseña_nueva.get()
        tipo = combo_tipo.get()

        if not nombre or not password or not tipo:
            messagebox.showwarning("Advertencia", "Complete todos los campos")
            return

        conexion = conectar_bd()
        if conexion is None:
            return
        cursor = conexion.cursor()

        try:
            cursor.execute(
                "INSERT INTO usuario (nombre, contraseña, tipo) VALUES (%s, %s, %s)",
                (nombre, password, tipo)
            )
            id_usuario = cursor.lastrowid

            if tipo.lower() == "admin":
                cursor.execute("INSERT INTO admin (id_usuario) VALUES (%s)", (id_usuario,))
            elif tipo.lower() == "empleado":
                cursor.execute(
                    "INSERT INTO empleado (id_usuario, rol, dni, nombre) VALUES (%s, %s, %s, %s)",
                    (id_usuario, "Vendedor", "00000000", nombre)
                )

            conexion.commit()
            messagebox.showinfo("Éxito", "Usuario creado correctamente")
            ventana_crear.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo crear el usuario:\n{err}")
        finally:
            cursor.close()
            conexion.close()

    ventana_crear = tk.Toplevel(ventana)
    ventana_crear.title("Crear nuevo usuario")
    ventana_crear.geometry("420x440")
    ventana_crear.configure(bg="#fff3e0")
    centrar_ventana(ventana_crear, 420, 440)
    tk.Label(ventana_crear, text="Crear nuevo usuario", bg="#fff3e0", fg="#e67e22",
             font=("Segoe UI", 12, "bold")).pack(pady=10)

    tk.Label(ventana_crear, text="Nombre:", bg="#fff3e0").pack(pady=5)
    entry_nombre_nuevo = tk.Entry(ventana_crear, bd=1, relief="solid")
    entry_nombre_nuevo.pack()

    tk.Label(ventana_crear, text="Contraseña:", bg="#fff3e0").pack(pady=5)
    entry_contraseña_nueva = tk.Entry(ventana_crear, show="*", bd=1, relief="solid")
    entry_contraseña_nueva.pack()

    tk.Label(ventana_crear, text="Tipo (admin/empleado):", bg="#fff3e0").pack(pady=5)
    combo_tipo = tk.Entry(ventana_crear, bd=1, relief="solid")
    combo_tipo.pack()

    tk.Button(ventana_crear, text="Guardar usuario", command=guardar_usuario,
              bg="#f9a66c", fg="white", activebackground="#e58e26",
              font=("Segoe UI", 10, "bold"), relief="flat", width=20, height=1).pack(pady=15)

# ----------------- CENTRAR VENTANA -----------------
def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# ----------------- TOGGLE MOSTRAR CONTRASEÑA -----------------
def toggle_contraseña():
    if var_mostrar.get():
        entry_contraseña.config(show="")
    else:
        entry_contraseña.config(show="*")

# ----------------- INTERFAZ PRINCIPAL -----------------
ventana = tk.Tk()
ventana.title("Login - Kiosco")
ancho, alto = 720, 500
centrar_ventana(ventana, ancho, alto)
ventana.configure(bg="#fff3e0")

# Título
tk.Label(ventana, text="Bienvenido al Kiosco", bg="#fff3e0", fg="#271a0f",
         font=("Segoe UI", 14, "bold")).pack(pady=15)

# Usuario
tk.Label(ventana, text="Usuario:", bg="#fff3e0", font=("Segoe UI", 10)).pack(pady=5)
entry_usuario = tk.Entry(ventana, width=25, bd=1, relief="solid")
entry_usuario.pack()

# Contraseña
tk.Label(ventana, text="Contraseña:", bg="#fff3e0", font=("Segoe UI", 10)).pack(pady=5)
entry_contraseña = tk.Entry(ventana, width=25, show="*", bd=1, relief="solid")
entry_contraseña.pack()

# Checkbox mostrar contraseña
var_mostrar = tk.BooleanVar()
tk.Checkbutton(ventana, text="Mostrar contraseña", variable=var_mostrar,
               command=toggle_contraseña, bg="#fff3e0").pack(pady=5)

# Botones
tk.Button(ventana, text="Iniciar sesión", command=iniciar_sesion,
          bg="#22180f", fg="white", font=("Segoe UI", 10, "bold"),
          relief="flat", width=20, height=1, activebackground="#ca7e1a").pack(pady=10)

tk.Button(ventana, text="Crear nuevo usuario", command=crear_usuario,
          bg="#22180f", fg="white", font=("Segoe UI", 10, "bold"),
          relief="flat", width=20, height=1, activebackground="#ca7e1a").pack(pady=5)

ventana.mainloop()
