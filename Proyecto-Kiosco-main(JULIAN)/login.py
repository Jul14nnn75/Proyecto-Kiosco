import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_APP = os.path.join(BASE_DIR, "main_app.py")
GESTION_TURNOS = os.path.join(BASE_DIR, "turno3.py")

def center_window(win, width=600, height=400):
    win.update_idletasks()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

def launch_app(script_path, wait=False):
    """Ejecuta un script Python en un nuevo proceso. Si wait=True, espera a que finalice."""
    if not os.path.exists(script_path):
        messagebox.showerror("Error", f"No se encontró {os.path.basename(script_path)}")
        return
    try:
        if wait:
            subprocess.run([sys.executable, script_path], cwd=BASE_DIR)
        else:
            subprocess.Popen([sys.executable, script_path], cwd=BASE_DIR)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo iniciar la aplicación:\n{e}")

def validate_and_proceed(role_var, pwd_entry, root):
    role = role_var.get()
    pwd = pwd_entry.get()

    if role == "Administrador":
        if pwd == "Admin":
            root.destroy()
            launch_app(MAIN_APP)
        else:
            messagebox.showerror("Credenciales inválidas", "Contraseña incorrecta para Administrador.")
    elif role == "Empleado":
        if pwd == "empleado":
            root.destroy()
            # Primero gestion_turnos, luego main_app
            launch_app(GESTION_TURNOS, wait=True)
            launch_app(MAIN_APP)
        else:
            messagebox.showerror("Credenciales inválidas", "Contraseña incorrecta para Empleado.")
    else:
        messagebox.showwarning("Rol no seleccionado", "Seleccione un rol: Administrador o Empleado.")

def show_login():
    root = tk.Tk()
    root.title("Ingreso al Sistema - Kiosco")
    root.resizable(False, False)

    # 🎨 Estilo naranja pastel minimalista
    bg_color = "#FFE5B4"  # naranja pastel suave
    card_color = "#FFFFFF"
    accent_color = "#FFB347"  # naranja más fuerte

    root.configure(bg=bg_color)
    center_window(root, 600, 400)

    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except:
        pass

    style.configure("TFrame", background=bg_color)
    style.configure("Card.TFrame", background=card_color, relief="flat")
    style.configure("TLabel", background=card_color, font=("Segoe UI", 12))
    style.configure("Header.TLabel", background=card_color, font=("Segoe UI", 18, "bold"))
    style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=8)
    style.map("TButton",
              background=[("active", accent_color), ("!active", accent_color)],
              foreground=[("active", "white"), ("!active", "black")])

    # 🧱 Contenedor central
    container = ttk.Frame(root, style="TFrame", padding=20)
    container.pack(expand=True, fill="both")

    card = ttk.Frame(container, style="Card.TFrame", padding=30)
    card.place(relx=0.5, rely=0.5, anchor="center")

    ttk.Label(card, text="Bienvenido al Sistema del Kiosco", style="Header.TLabel").grid(
        row=0, column=0, columnspan=2, pady=(0, 25)
    )

    ttk.Label(card, text="Usuario:").grid(row=1, column=0, sticky="w", pady=8, padx=10)
    user_entry = ttk.Entry(card, width=35, font=("Segoe UI", 11))
    user_entry.grid(row=1, column=1, pady=8, padx=10)

    ttk.Label(card, text="Contraseña:").grid(row=2, column=0, sticky="w", pady=8, padx=10)
    pwd_entry = ttk.Entry(card, show="*", width=35, font=("Segoe UI", 11))
    pwd_entry.grid(row=2, column=1, pady=8, padx=10)

    ttk.Label(card, text="Rol:").grid(row=3, column=0, sticky="w", pady=8, padx=10)
    role_var = tk.StringVar(value="Empleado")
    roles_frame = ttk.Frame(card, style="Card.TFrame")
    roles_frame.grid(row=3, column=1, sticky="w")
    ttk.Radiobutton(roles_frame, text="Administrador", variable=role_var, value="Administrador").pack(side="left", padx=5)
    ttk.Radiobutton(roles_frame, text="Empleado", variable=role_var, value="Empleado").pack(side="left", padx=5)

    btn_frame = ttk.Frame(card, style="Card.TFrame")
    btn_frame.grid(row=4, column=0, columnspan=2, pady=(25, 0))

    def on_enter(event=None):
        validate_and_proceed(role_var, pwd_entry, root)

    ingresar_btn = ttk.Button(btn_frame, text="Ingresar", command=on_enter)
    ingresar_btn.pack(side="left", padx=15)

    salir_btn = ttk.Button(btn_frame, text="Salir", command=root.destroy)
    salir_btn.pack(side="left", padx=15)

    root.bind("<Return>", on_enter)
    user_entry.focus_set()

    root.mainloop()

if __name__ == "__main__":
    show_login()
