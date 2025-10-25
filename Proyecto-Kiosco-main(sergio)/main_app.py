import tkinter as tk
from tkinter import messagebox
from turno3 import TurnoUI
from caja import CajaApp
from reporte import abrir_reportes  # ✅ Importamos el nuevo módulo de reportes


class SistemaKiosco(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Kiosco - Menú Principal")
        self.state("zoomed")
        self.configure(bg="#0f5296")

        # Eliminamos toda la lógica de caja duplicada
        self.ventana_caja = None
        self.ventana_turnos = None
        self.ventana_inventario = None

        self.crear_interfaz()
        
        # ✅ Agregar confirmación al cerrar con la X
        self.protocol("WM_DELETE_WINDOW", self.confirmar_salida)

    # =============================
    #  INTERFAZ PRINCIPAL
    # =============================
    def crear_interfaz(self):
        main_frame = tk.Frame(self, bg="#1e9fdb")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        titulo = tk.Label(main_frame, text="Sistema de Kiosco",
                          font=("Futura", 35, "bold"))
        titulo.pack(pady=30)

        botones_frame = tk.Frame(main_frame, bg="#0f5296")
        botones_frame.pack(expand=True)

        # ✅ ELIMINADO Configuración, AGREGADO Reportes
        botones = [
            ("💰 Gestión de Caja", self.abrir_caja, "#7916a0"),
            ("📦 Inventario", self.abrir_inventario, "#7916a0"),
            ("👥 Gestión de Turnos", self.abrir_turnos, "#2112f3"),
            ("📊 Reportes", self.abrir_reportes, "#2112f3"),  # ✅ NUEVO
            
        ]

        for i, (texto, comando, color) in enumerate(botones):
            btn = tk.Button(botones_frame, text=texto, command=comando,
                            font=("Arial", 14, "bold"),
                            bg=color, fg="white",
                            width=20, height=2,
                            relief="raised", bd=3)
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky="nsew")

        for c in range(2):
            botones_frame.columnconfigure(c, weight=1)
        for r in range(3):
            botones_frame.rowconfigure(r, weight=1)

        self.barra_estado = tk.Label(self, text="Sistema listo - © 2025 Kiosco System",
                                     relief="sunken", anchor="w",
                                     font=("Arial", 10), bg="#34495e", fg="white")
        self.barra_estado.pack(side="bottom", fill="x")

    def confirmar_salida(self):
        """✅ Muestra confirmación antes de cerrar el sistema"""
        respuesta = messagebox.askyesno(
            "Confirmar Salida",
            "¿Está seguro que desea salir del sistema?",
            icon="question",
            default="no"
        )
        
        if respuesta:
            # Cerrar también las ventanas hijas si están abiertas
            if self.ventana_caja and self.ventana_caja.winfo_exists():
                self.ventana_caja.destroy()
            if self.ventana_turnos and self.ventana_turnos.winfo_exists():
                self.ventana_turnos.destroy()
            if self.ventana_inventario and self.ventana_inventario.winfo_exists():
                self.ventana_inventario.destroy()
            self.destroy()

    # =============================
    #  GESTIÓN DE CAJA (USANDO caja.py)
    # =============================
    def abrir_caja(self):
        """Abre el sistema de caja unificado desde caja.py"""
        if self.ventana_caja and self.ventana_caja.winfo_exists():
            self.ventana_caja.lift()
            self.ventana_caja.focus_force()
            return

        # ✅ Usamos la CajaApp original que ya tiene toda la lógica
        self.ventana_caja = CajaApp()
        # Configuramos para que sea hija de la ventana principal
        self.ventana_caja.transient(self)
        self.ventana_caja.grab_set()
        
        # Centramos la ventana de caja relativa a la principal
        self.ventana_caja.geometry("+100+100")

    # =============================
    #  OTROS MÓDULOS
    # =============================
    def abrir_inventario(self):
        """Abre el módulo de inventario"""
        try:
            if self.ventana_inventario and self.ventana_inventario.winfo_exists():
                self.ventana_inventario.lift()
                self.ventana_inventario.focus_force()
                return

            # ✅ Importar y abrir inventario
            from inventario import InventarioApp
            
            # Crear ventana para inventario
            self.ventana_inventario = tk.Toplevel(self)
            self.ventana_inventario.title("📦 Inventario - Kiosco")
            self.ventana_inventario.geometry("900x700")
            self.ventana_inventario.resizable(False, False)
            self.ventana_inventario.transient(self)
            self.ventana_inventario.grab_set()
            
            # Centrar ventana
            x = self.winfo_x() + (self.winfo_width() - 900) // 2
            y = self.winfo_y() + (self.winfo_height() - 700) // 2
            self.ventana_inventario.geometry(f"+{x}+{y}")
            
            # ✅ Inicializar InventarioApp en la ventana
            InventarioApp(self.ventana_inventario)
            
        except ImportError as e:
            messagebox.showerror("Error", f"No se pudo encontrar el módulo de inventario:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el inventario:\n{str(e)}")

    def abrir_turnos(self):
        """Abre la gestión de turnos"""
        try:
            if self.ventana_turnos and self.ventana_turnos.winfo_exists():
                self.ventana_turnos.lift()
                self.ventana_turnos.focus_force()
                return

            # ✅ Crear ventana para turnos
            self.ventana_turnos = tk.Toplevel(self)
            self.ventana_turnos.title("Gestión de Turnos")
            self.ventana_turnos.geometry("800x600")
            self.ventana_turnos.transient(self)
            self.ventana_turnos.grab_set()
            self.ventana_turnos.focus_force()
            
            # Centrar ventana
            x = self.winfo_x() + (self.winfo_width() - 800) // 2
            y = self.winfo_y() + (self.winfo_height() - 600) // 2
            self.ventana_turnos.geometry(f"+{x}+{y}")
            
            TurnoUI(master=self.ventana_turnos)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la gestión de turnos:\n{str(e)}")

    def abrir_reportes(self):
        """Abre la ventana de reportes"""
        try:
            # ✅ Usar la función importada de reporte.py
            abrir_reportes(self)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir los reportes:\n{str(e)}")

    def salir_sistema(self):
        if messagebox.askyesno("Salir", "¿Está seguro que desea salir del sistema?"):
            # Cerramos también la ventana de caja si está abierta
            if self.ventana_caja and self.ventana_caja.winfo_exists():
                self.ventana_caja.destroy()
            if self.ventana_turnos and self.ventana_turnos.winfo_exists():
                self.ventana_turnos.destroy()
            if self.ventana_inventario and self.ventana_inventario.winfo_exists():
                self.ventana_inventario.destroy()
            self.destroy()


if __name__ == "__main__":
    app = SistemaKiosco()
    app.mainloop()