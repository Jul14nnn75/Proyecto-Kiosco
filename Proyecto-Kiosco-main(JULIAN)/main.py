import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import os
from turno3 import TurnoUI


class SistemaKiosco(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Kiosco - Menú Principal")
        self.state("zoomed")
        self.configure(bg="#2c3e50")

        # Estados de caja
        self.saldo_inicial = 0.0
        self.total_ventas = 0.0
        self.retiros = 0.0
        self.ingresos = 0.0
        self.gastos = 0.0
        self.caja_abierta = False

        # Referencias
        self.ventana_caja = None
        self.resumen_labels = {}

        self.crear_interfaz()

    # =============================
    #  INTERFAZ PRINCIPAL
    # =============================
    def crear_interfaz(self):
        main_frame = tk.Frame(self, bg="#2c3e50")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        titulo = tk.Label(main_frame, text="SISTEMA DE KIOSCO",
                          font=("Arial", 24, "bold"), fg="white", bg="#2c3e50")
        titulo.pack(pady=30)

        botones_frame = tk.Frame(main_frame, bg="#2c3e50")
        botones_frame.pack(expand=True)

        botones = [
            ("💰 Gestión de Caja", self.abrir_caja, "#27ae60"),
            ("📦 Inventario", self.abrir_inventario, "#16a085"),
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
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky="nsew")

        for c in range(2):
            botones_frame.columnconfigure(c, weight=1)
        for r in range(3):
            botones_frame.rowconfigure(r, weight=1)

        self.barra_estado = tk.Label(self, text="Sistema listo - © 2025 Kiosco System",
                                     relief="sunken", anchor="w",
                                     font=("Arial", 10), bg="#34495e", fg="white")
        self.barra_estado.pack(side="bottom", fill="x")

    # =============================
    #  GESTIÓN DE CAJA
    # =============================
    def abrir_caja(self):
        if self.ventana_caja and self.ventana_caja.winfo_exists():
            self.ventana_caja.lift()
            return

        ventana = tk.Toplevel(self)
        ventana.title("Gestión de Caja")
        ventana.geometry("900x500")
        ventana.configure(bg="#ffeaa7")

        contenedor = tk.Frame(ventana, bg="#ffeaa7")
        contenedor.pack(expand=True, fill="both", padx=20, pady=20)

        # Panel izquierdo
        panel_izq = tk.Frame(contenedor, bg="#ffeaa7")
        panel_izq.pack(side="left", fill="y", padx=10)

        botones = [
            ("[F1] Facturar", self.facturar),
            ("[F2] Apertura", self.abrir_apertura),
            ("[F3] Retiro", self.abrir_retiro),
            ("[F4] Gastos", self.abrir_gastos),
            ("[F5] Ingreso", self.abrir_ingreso),
            ("[F6] Cierre Caja", self.cierre_caja),
            ("[F7] Imprimir", self.imprimir),
            ("[ESC] Salir", ventana.destroy)
        ]

        for i, (texto, accion) in enumerate(botones):
            btn = tk.Button(panel_izq, text=texto, font=("Arial", 12, "bold"),
                            bg="#d35400", fg="white", width=20, height=2,
                            relief="raised", bd=3, command=accion)
            btn.grid(row=i, column=0, pady=6, sticky="ew")
            ventana.bind("<Return>", lambda e, b=btn: b.invoke())

        # Panel derecho (Resumen)
        panel_der = tk.Frame(contenedor, bg="#ffeaa7")
        panel_der.pack(side="left", expand=True, fill="both", padx=30)

        tk.Label(panel_der, text="Resumen de Caja",
                 font=("Arial", 16, "bold"),
                 bg="#ffeaa7", fg="#2c3e50").pack(pady=10)

        datos = [
            ("Saldo Inicial:", "saldo_inicial"),
            ("Total Ventas:", "total_ventas"),
            ("Retiros:", "retiros"),
            ("Ingresos:", "ingresos"),
            ("Gastos:", "gastos")
        ]

        for texto, var in datos:
            fila = tk.Frame(panel_der, bg="#ffeaa7")
            fila.pack(fill="x", pady=5)
            tk.Label(fila, text=texto, font=("Arial", 12, "bold"),
                     width=15, anchor="e", bg="#ffeaa7", fg="#2c3e50").pack(side="left")
            lbl_valor = tk.Label(fila, text="$0.00", font=("Arial", 12),
                                 anchor="w", bg="#ffeaa7", fg="#2c3e50")
            lbl_valor.pack(side="left")
            self.resumen_labels[var] = lbl_valor

        self.ventana_caja = ventana

    # =============================
    #  FUNCIONES DE CAJA
    # =============================
    def abrir_apertura(self):
        """Abre la ventana de apertura sin mostrar mensajes."""
        def confirmar():
            try:
                monto = float(entrada.get())
                self.saldo_inicial = monto
                self.caja_abierta = True
                self._actualizar_resumen()
                win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Ingrese un monto válido.")

        win = tk.Toplevel(self)
        win.title("Apertura de Caja")
        win.geometry("300x150")
        win.configure(bg="#ecf0f1")

        tk.Label(win, text="Monto de apertura ($):", font=("Arial", 12, "bold"), bg="#ecf0f1").pack(pady=10)
        entrada = tk.Entry(win, font=("Arial", 12))
        entrada.pack(pady=5)
        entrada.focus()

        btn = tk.Button(win, text="Confirmar", bg="#27ae60", fg="white", font=("Arial", 12), command=confirmar)
        btn.pack(pady=10)
        win.bind("<Return>", lambda e: confirmar())

    def abrir_retiro(self):
        self._crear_ventana_valor("Retiro de Caja", "Monto a retirar ($):", "retiros")

    def abrir_gastos(self):
        self._crear_ventana_valor("Registrar Gasto", "Monto del gasto ($):", "gastos")

    def abrir_ingreso(self):
        self._crear_ventana_valor("Registrar Ingreso", "Monto del ingreso ($):", "ingresos")

    def _crear_ventana_valor(self, titulo, etiqueta, tipo):
        win = tk.Toplevel(self)
        win.title(titulo)
        win.geometry("300x150")
        win.configure(bg="#ecf0f1")

        tk.Label(win, text=etiqueta, font=("Arial", 12, "bold"), bg="#ecf0f1").pack(pady=10)
        entrada = tk.Entry(win, font=("Arial", 12))
        entrada.pack(pady=5)
        entrada.focus()

        def aceptar():
            try:
                monto = float(entrada.get())
                setattr(self, tipo, getattr(self, tipo) + monto)
                self._actualizar_resumen()
                win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Ingrese un monto válido.")

        btn = tk.Button(win, text="Aceptar", bg="#27ae60", fg="white", font=("Arial", 12), command=aceptar)
        btn.pack(pady=10)
        win.bind("<Return>", lambda e: aceptar())

    def cierre_caja(self):
        """Ventana de cierre de caja con cálculo, guardado y reseteo."""
        saldo_sistema = self.saldo_inicial + self.ingresos - self.retiros - self.gastos + self.total_ventas

        win = tk.Toplevel(self)
        win.title("Cierre de Caja")
        win.geometry("420x340")
        win.configure(bg="#ecf0f1")

        tk.Label(win, text="Cierre de Caja", font=("Arial", 16, "bold"), bg="#ecf0f1").pack(pady=10)
        tk.Label(win, text=f"💻 Saldo del sistema: ${saldo_sistema:.2f}",
                 font=("Arial", 13, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=5)

        frame_inputs = tk.Frame(win, bg="#ecf0f1")
        frame_inputs.pack(pady=10)

        tk.Label(frame_inputs, text="Importe de caja (efectivo):", font=("Arial", 12),
                 bg="#ecf0f1").grid(row=0, column=0, sticky="e", pady=5, padx=5)
        entrada_caja = tk.Entry(frame_inputs, font=("Arial", 12))
        entrada_caja.grid(row=0, column=1, pady=5, padx=5)
        entrada_caja.focus()

        tk.Label(frame_inputs, text="Saldo transferencia:", font=("Arial", 12),
                 bg="#ecf0f1").grid(row=1, column=0, sticky="e", pady=5, padx=5)
        entrada_transferencia = tk.Entry(frame_inputs, font=("Arial", 12))
        entrada_transferencia.grid(row=1, column=1, pady=5, padx=5)

        lbl_diferencia = tk.Label(win, text="Diferencia: $0.00",
                                  font=("Arial", 13, "bold"),
                                  bg="#ecf0f1", fg="#2c3e50")
        lbl_diferencia.pack(pady=10)

        def confirmar_cierre():
            try:
                importe_caja = float(entrada_caja.get() or 0)
                saldo_transferencia = float(entrada_transferencia.get() or 0)
                diferencia = saldo_sistema - (importe_caja + saldo_transferencia)
                self.caja_abierta = False

                if not os.path.exists("cierres"):
                    os.makedirs("cierres")

                ruta = os.path.join("cierres", "cierres.csv")
                existe = os.path.isfile(ruta)

                with open(ruta, "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    if not existe:
                        writer.writerow(["Fecha", "Saldo Sistema", "Importe Caja", "Saldo Transferencia", "Diferencia"])
                    writer.writerow([
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        f"{saldo_sistema:.2f}",
                        f"{importe_caja:.2f}",
                        f"{saldo_transferencia:.2f}",
                        f"{diferencia:.2f}"
                    ])

                messagebox.showinfo(
                    "Cierre de Caja",
                    f"💻 Saldo del sistema: ${saldo_sistema:.2f}\n"
                    f"💵 Importe de caja: ${importe_caja:.2f}\n"
                    f"🏦 Saldo transferencia: ${saldo_transferencia:.2f}\n"
                    f"📊 Diferencia: ${diferencia:.2f}\n\n"
                    f"✅ Guardado en cierres/cierres.csv"
                )

                # 🔁 Resetear saldos
                self.saldo_inicial = 0.0
                self.total_ventas = 0.0
                self.retiros = 0.0
                self.ingresos = 0.0
                self.gastos = 0.0
                self._actualizar_resumen()

                win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Ingrese montos válidos.")

        tk.Button(win, text="Cerrar Caja", bg="#27ae60", fg="white",
                  font=("Arial", 12), width=18, command=confirmar_cierre).pack(pady=10)

        win.bind("<Return>", lambda e: confirmar_cierre())

    # =============================
    #  OTROS
    # =============================
    def imprimir(self):
        messagebox.showinfo("Imprimir", "Imprimiendo resumen de caja...")

    def facturar(self):
        if not self.caja_abierta:
            messagebox.showwarning("Atención", "Debe abrir la caja antes de facturar.")
            return
        try:
            from ventana import POSWindow
            ventana_factura = POSWindow(self)
            ventana_factura.grab_set()
            ventana_factura.focus_force()
        except Exception as e:
            import traceback
            messagebox.showerror("Error", f"No se pudo abrir la facturación:\n\n{e}\n\n{traceback.format_exc()}")

    def abrir_inventario(self):
        messagebox.showinfo("Inventario", "Módulo en desarrollo")

    def abrir_turnos(self):
        ventana_turnos = tk.Toplevel(self)
        ventana_turnos.title("Gestion de Turnos")
        ventana_turnos.geometry("800x600")
        ventana_turnos.transient(self)
        ventana_turnos.grab_set()
        ventana_turnos.focus_force()
        TurnoUI(master=ventana_turnos)

    def mostrar_reportes(self):
        messagebox.showinfo("Reportes", "Módulo en desarrollo")

    def mostrar_configuracion(self):
        messagebox.showinfo("Configuración", "Módulo en desarrollo")

    def _actualizar_resumen(self):
        self.resumen_labels["saldo_inicial"].config(text=f"${self.saldo_inicial:.2f}")
        self.resumen_labels["total_ventas"].config(text=f"${self.total_ventas:.2f}")
        self.resumen_labels["retiros"].config(text=f"${self.retiros:.2f}")
        self.resumen_labels["ingresos"].config(text=f"${self.ingresos:.2f}")
        self.resumen_labels["gastos"].config(text=f"${self.gastos:.2f}")

    def salir_sistema(self):
        if messagebox.askyesno("Salir", "¿Está seguro que desea salir del sistema?"):
            self.destroy()


if __name__ == "__main__":
    app = SistemaKiosco()
    app.mainloop()
