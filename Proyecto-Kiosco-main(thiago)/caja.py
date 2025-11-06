import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import json
from cajaAux import CajaPopup, popup_cierre_caja
from ventana import POSWindow  # tu ventana de facturación

class CajaApp(tk.Tk):
    ESTADO_PATH = os.path.join("data", "estado_caja.json")

    def __init__(self):
        super().__init__()
        self.title("💰 Gestión de Caja")
        self.monto_apertura = None
        self.saldo_sistema = 0
        self.ventas_realizadas = []

        # Variables para registrar operaciones individuales
        self.ingreso_actual = ("", 0)
        self.retiro_actual = ("", 0)
        self.gasto_actual = ("", 0)

        # Colores
        self.bg_color = "#FFE5B4"
        self.card_color = "#FFFFFF"
        self.accent_color = "#FFB347"
        self.text_color = "#2c3e50"
        self.success_color = "#27ae60"
        self.danger_color = "#e74c3c"

        # Configuración ventana
        ancho, alto = 320, 580
        y = (self.winfo_screenheight() - alto) // 2 - 150
        self.geometry(f"{ancho}x{alto}+50+{y}")
        self.resizable(False, False)
        self.configure(bg=self.bg_color)

        os.makedirs("data", exist_ok=True)

        self._configurar_estilo()
        self._crear_interfaz()
        self._cargar_estado()

        self.lift()
        self.attributes("-topmost", True)

        self.protocol("WM_DELETE_WINDOW", self._guardar_y_salir)

    # ---------- Estilo ----------
    def _configurar_estilo(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except:
            pass
        style.configure(
            "Caja.TButton",
            font=("Arial", 11, "bold"),
            padding=(10, 8),
            relief="flat",
            background=self.accent_color,
            foreground="white"
        )

    # ---------- Interfaz ----------
    def _crear_interfaz(self):
        main = tk.Frame(self, bg=self.bg_color, padx=15, pady=15)
        main.pack(fill="both", expand=True)

        tk.Label(main, text="💰 CAJA", font=("Arial", 20, "bold"),
                 bg=self.bg_color, fg=self.text_color).pack()
        tk.Label(main, text="Gestión de Efectivo", font=("Arial", 11),
                 bg=self.bg_color, fg=self.text_color).pack(pady=(0, 20))

        self.estado_label = tk.Label(main, text="🔒 CAJA CERRADA",
                                     font=("Arial", 12, "bold"),
                                     bg=self.danger_color, fg="white",
                                     padx=10, pady=8)
        self.estado_label.pack(fill="x", pady=(0, 15))

        botones = [
            ("📄 Facturar", self.accion_facturar, self.accent_color),
            ("📂 Apertura", self.accion_apertura, self.success_color),
            ("💸 Retiro", lambda: self._popup_operacion("Retiro de Caja", "retiro", "#e67e22"), "#e67e22"),
            ("📋 Gastos", lambda: self._popup_operacion("Registrar Gasto", "gasto", "#e74c3c"), "#e74c3c"),
            ("💳 Ingreso", lambda: self._popup_operacion("Ingreso de Caja", "ingreso", "#3498db"), "#3498db"),
            ("🔒 Cierre Caja", self.accion_cierre, "#9b59b6"),
            ("🚪 Salir", self._guardar_y_salir, "#95a5a6")
        ]

        for texto, comando, color in botones:
            f = tk.Frame(main, bg=self.bg_color, height=55)
            f.pack(fill="x", pady=4)
            f.pack_propagate(False)
            btn = tk.Button(f, text=texto, command=comando, font=("Arial", 11, "bold"),
                            bg=color, fg="white", relief="flat", bd=0,
                            cursor="hand2", padx=15, pady=12, anchor="w")
            btn.pack(fill="both", expand=True, padx=2)
            btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(bg=self._oscurecer(c, 20)))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))

    # ---------- Utilidades ----------
    def _oscurecer(self, color, amt):
        c = color.lstrip("#")
        r, g, b = [max(0, int(c[i:i+2], 16) - amt) for i in (0, 2, 4)]
        return f"#{r:02x}{g:02x}{b:02x}"

    def _actualizar_estado(self):
        if self.monto_apertura is not None:
            self.estado_label.config(
                text=f"✅ CAJA ABIERTA - ${self.saldo_sistema:.2f}",
                bg=self.success_color
            )
        else:
            self.estado_label.config(
                text="🔒 CAJA CERRADA",
                bg=self.danger_color
            )

    # ---------- Persistencia ----------
    def _guardar_estado(self):
        estado = {
            "abierta": self.monto_apertura is not None,
            "monto_apertura": self.monto_apertura if self.monto_apertura else 0,
            "saldo_sistema": self.saldo_sistema,
            "ventas": self.ventas_realizadas,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(self.ESTADO_PATH, "w", encoding="utf-8") as f:
            json.dump(estado, f, indent=4)

    def _cargar_estado(self):
        if os.path.isfile(self.ESTADO_PATH):
            with open(self.ESTADO_PATH, "r", encoding="utf-8") as f:
                estado = json.load(f)
                if estado.get("abierta", False):
                    self.monto_apertura = estado.get("monto_apertura", 0)
                    self.saldo_sistema = estado.get("saldo_sistema", 0)
                    self.ventas_realizadas = estado.get("ventas", [])
                    self._actualizar_estado()

    def _guardar_y_salir(self):
        if self.monto_apertura is not None:
            self._guardar_estado()
        self.destroy()

    # ---------- Acciones ----------
    def accion_facturar(self):
        if not self.monto_apertura:
            messagebox.showerror("Error", "Debe abrir la caja antes de facturar.")
            return
        ventana = POSWindow(caja=self)
        ventana.transient(self)
        ventana.grab_set()
        ventana.geometry("1000x650+350+200")

    def accion_apertura(self):
        if self.monto_apertura is not None:
            messagebox.showerror("Error", "La caja ya está abierta.")
            return
        CajaPopup(self, "Apertura de Caja", "apertura", self.success_color, self._set_apertura)

    def _set_apertura(self, monto, motivo):
        self.monto_apertura = monto
        self.saldo_sistema = monto  # Apertura suma al saldo
        self.ventas_realizadas = []
        self._actualizar_estado()
        self._guardar_estado()

    def _popup_operacion(self, titulo, tipo, color):
        if not self.monto_apertura:
            messagebox.showerror("Error", "Debe abrir la caja primero.")
            return
        CajaPopup(self, titulo, tipo, color)

    def accion_cierre(self):
        if not self.monto_apertura:
            messagebox.showerror("Error", "Debe abrir la caja para cerrarla.")
            return
        popup_cierre_caja(self)

    # ---------- Integración con Ventana de Venta ----------
    def _registrar_venta_en_caja(self, total, detalles):
        try:
            total_num = float(total)
        except:
            try:
                total_num = float(str(total).replace(",", "."))
            except:
                total_num = 0.0
        self.saldo_sistema += total_num
        self.ventas_realizadas.append({
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": total_num,
            "detalles": detalles
        })
        self._guardar_estado()
        self._actualizar_estado()

    def accion_salir(self):
        self._guardar_y_salir()


if __name__ == "__main__":
    app = CajaApp()
    app.mainloop()
