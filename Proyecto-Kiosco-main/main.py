import tkinter as tk
from tkinter import Menu, messagebox
import subprocess
import sys
import os

class SistemaKiosco(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Kiosco - Menú Principal")
        self.geometry("800x600")
        self.configure(bg="#2c3e50")
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Frame principal
        main_frame = tk.Frame(self, bg="#2c3e50")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Título
        titulo = tk.Label(main_frame, text="SISTEMA DE KIOSCO", 
                         font=("Arial", 24, "bold"), 
                         fg="white", bg="#2c3e50")
        titulo.pack(pady=30)
        
        # Frame de botones
        botones_frame = tk.Frame(main_frame, bg="#2c3e50")
        botones_frame.pack(expand=True)
        
        # Botones principales
        botones = [
            ("🏪 Punto de Venta", self.abrir_punto_venta, "#e74c3c"),
            ("💰 Gestión de Caja", self.abrir_caja, "#27ae60"),
            ("👥 Gestión de Turnos", self.abrir_turnos, "#3498db"),
            ("📊 Reportes", self.mostrar_reportes, "#f39c12"),
            ("⚙️ Configuración", self.mostrar_configuracion, "#9b59b6"),
            ("❌ Salir", self.salir_sistema, "#95a5a6")
        ]
        
        for i, (texto, comando, color) in enumerate(botones):
            btn = tk.Button(botones_frame, text=texto, command=comando,
                          font=("Arial", 14, "bold"), 
                          bg=color, fg="white",
                          width=20, height=2,
                          relief="raised", bd=3)
            btn.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
            
        # Configurar grid
        botones_frame.columnconfigure(0, weight=1)
        botones_frame.columnconfigure(1, weight=1)
        botones_frame.rowconfigure(0, weight=1)
        botones_frame.rowconfigure(1, weight=1)
        botones_frame.rowconfigure(2, weight=1)
        
        # Barra de estado
        self.barra_estado = tk.Label(self, text="Sistema listo - © 2024 Kiosco System", 
                                    relief="sunken", anchor="w",
                                    font=("Arial", 10), bg="#34495e", fg="white")
        self.barra_estado.pack(side="bottom", fill="x")
        
    def abrir_punto_venta(self):
        try:
            from ventana import POSWindow  # CORREGIDO: Indentación correcta
            ventana_venta = POSWindow(self)
            ventana_venta.grab_set()
        except ImportError as e:
            messagebox.showerror("Error", f"No se pudo abrir el punto de venta: {e}")
            
    def abrir_caja(self):
        try:
            from caja import CajaApp
            ventana_caja = CajaApp()
            ventana_caja.grab_set()
        except ImportError as e:
            messagebox.showerror("Error", f"No se pudo abrir la caja: {e}")
            
    def abrir_turnos(self):
        try:
            from turno3 import TurnoUI
            ventana_turnos = tk.Toplevel(self)
            ventana_turnos.title("Gestión de Turnos")
            ventana_turnos.geometry("800x600")
            app_turnos = TurnoUI(ventana_turnos)
            app_turnos.pack(fill="both", expand=True)
        except ImportError as e:
            messagebox.showerror("Error", f"No se pudo abrir gestión de turnos: {e}")
            
    def mostrar_reportes(self):
        messagebox.showinfo("Reportes", "Módulo de reportes en desarrollo")
        
    def mostrar_configuracion(self):
        messagebox.showinfo("Configuración", "Módulo de configuración en desarrollo")
        
    def salir_sistema(self):
        if messagebox.askyesno("Salir", "¿Está seguro que desea salir del sistema?"):
            self.destroy()

if __name__ == "__main__":
    app = SistemaKiosco()
    app.mainloop()