# 📁 sistema_kiosco.py (versión corregida y más robusta)
import tkinter as tk
from tkinter import messagebox
from turno3 import TurnoUI
from caja import CajaApp
from reporte import abrir_reportes
from inventario import InventarioApp


class SistemaKiosco(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Kiosco - Menú Principal")
        self.state("zoomed")
        self.configure(bg="#0f5296")

        # Referencias a ventanas
        self.ventana_caja = None
        self.ventana_turnos = None
        self.ventana_inventario = None

        self.crear_interfaz()
        self.protocol("WM_DELETE_WINDOW", self.confirmar_salida)

    # ==============================
    # 🧩 INTERFAZ PRINCIPAL
    # ==============================
    def crear_interfaz(self):
        main_frame = tk.Frame(self, bg="#1e9fdb")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        tk.Label(main_frame, text="Sistema de Kiosco",
                 font=("Futura", 35, "bold"), bg="#1e9fdb", fg="white").pack(pady=30)

        botones_frame = tk.Frame(main_frame, bg="#0f5296")
        botones_frame.pack(expand=True)

        botones = [
            ("💰 Gestión de Caja", self.abrir_caja, "#7916a0"),
            ("📦 Inventario", self.abrir_inventario, "#7916a0"),
            ("👥 Gestión de Turnos", self.abrir_turnos, "#2112f3"),
            ("📊 Reportes", self.abrir_reportes, "#2112f3"),
        ]

        for i, (texto, comando, color) in enumerate(botones):
            btn = tk.Button(botones_frame, text=texto, command=comando,
                            font=("Arial", 14, "bold"), bg=color, fg="white",
                            width=20, height=2, relief="raised", bd=3)
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky="nsew")

        self.barra_estado = tk.Label(self,
                                     text="Sistema listo - © 2025 Kiosco System",
                                     relief="sunken", anchor="w",
                                     font=("Arial", 10),
                                     bg="#34495e", fg="white")
        self.barra_estado.pack(side="bottom", fill="x")

    # ==============================
    # 💰 GESTIÓN DE CAJA
    # ==============================
    def abrir_caja(self):
        # Primero: limpiar referencia si la ventana quedó huérfana
        if self.ventana_caja:
            try:
                if not self.ventana_caja.winfo_exists():
                    # la ventana ya fue cerrada por el usuario -> limpiar referencia
                    self.ventana_caja = None
            except Exception:
                self.ventana_caja = None

        # Si ya existe una instancia válida -> traer al frente y asegurarse usable
        if self.ventana_caja and self.ventana_caja.winfo_exists():
            try:
                # Si la caja está "abierta" pero no tiene monto_apertura (None o 0),
                # no forzamos un nuevo popup que genere conflicto; simplemente mostramos la ventana.
                # Si CajaApp define un método mostrar_apertura() lo llamamos para abrir su diálogo interno.
                if hasattr(self.ventana_caja, "monto_apertura") and (self.ventana_caja.monto_apertura is None):
                    # intento preferente: método de CajaApp para abrir diálogo de apertura si existe
                    if hasattr(self.ventana_caja, "mostrar_apertura"):
                        try:
                            self.ventana_caja.mostrar_apertura()
                        except Exception:
                            # fallback suave
                            self.ventana_caja.deiconify()
                            self.ventana_caja.lift()
                            self.ventana_caja.focus_force()
                    else:
                        # fallback: solo mostrar ventana para que el operador pueda interactuar
                        self.ventana_caja.deiconify()
                        self.ventana_caja.lift()
                        self.ventana_caja.focus_force()
                else:
                    self.ventana_caja.deiconify()
                    self.ventana_caja.lift()
                    self.ventana_caja.focus_force()
            except Exception:
                # Si por alguna razón falló el bring-to-front, recreamos la ventana
                try:
                    self.ventana_caja.destroy()
                except:
                    pass
                self.ventana_caja = None

            return

        # Si no existe, crear una nueva instancia de CajaApp
        try:
            # Intentamos pasar 'self' como master si CajaApp lo acepta
            try:
                self.ventana_caja = CajaApp(master=self)
            except TypeError:
                # Si la clase CajaApp no acepta master en constructor, lo creamos sin args
                self.ventana_caja = CajaApp()
            # configurar comportamiento al cerrarse la ventana de caja
            try:
                self.ventana_caja.protocol("WM_DELETE_WINDOW", self._on_caja_closed)
            except Exception:
                pass
            # hacer modal/transient para UX coherente
            try:
                self.ventana_caja.transient(self)
                self.ventana_caja.grab_set()
            except Exception:
                pass
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la Gestión de Caja:\n{e}")
            self.ventana_caja = None

    def _on_caja_closed(self):
        """Handler para cuando la ventana de caja se cierra por su propio botón X."""
        try:
            if self.ventana_caja and self.ventana_caja.winfo_exists():
                self.ventana_caja.destroy()
        except:
            pass
        # limpiar referencia para permitir reabrirla
        self.ventana_caja = None

    # ==============================
    # 📦 INVENTARIO
    # ==============================
    def abrir_inventario(self):
        if self.ventana_inventario and self.ventana_inventario.winfo_exists():
            self.ventana_inventario.lift()
            return
        win = tk.Toplevel(self)
        win.title("📦 Inventario - Kiosco")
        win.geometry("900x700")
        win.resizable(False, False)
        InventarioApp(win)
        win.transient(self)
        win.grab_set()

    # ==============================
    # 👥 TURNOS
    # ==============================
    def abrir_turnos(self):
        if self.ventana_turnos and self.ventana_turnos.winfo_exists():
            self.ventana_turnos.lift()
            return
        win = tk.Toplevel(self)
        win.title("Gestión de Turnos")
        win.geometry("800x600")
        TurnoUI(master=win)
        win.transient(self)
        win.grab_set()

    # ==============================
    # 📊 REPORTES
    # ==============================
    def abrir_reportes(self):
        try:
            abrir_reportes(self)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron abrir los reportes:\n{e}")

    # ==============================
    # 🚪 SALIDA
    # ==============================
    def confirmar_salida(self):
        if messagebox.askyesno("Salir", "¿Está seguro que desea salir del sistema?"):
            # Cerrar todas las ventanas hijas abiertas
            for ventana in [self.ventana_caja, self.ventana_turnos, self.ventana_inventario]:
                try:
                    if ventana and ventana.winfo_exists():
                        ventana.destroy()
                except:
                    pass
            self.destroy()


if __name__ == "__main__":
    SistemaKiosco().mainloop()
