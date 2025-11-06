import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import json
from cajaAux import VentanaEmergenteCaja, ventana_cierre_caja
from ventana import POSWindow

class CajaApp(tk.Tk):
    ESTADO_PATH = os.path.join("data", "estado_caja.json")

    def __init__(self):
        super().__init__()
        self.title("CAJA")
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

        # 🔥 POSICIÓN: Abajo y a la izquierda
        ancho, alto = 300, 450
        x = 30
        y = 400
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")

        os.makedirs("data", exist_ok=True)

        self._crear_interfaz()
        self._cargar_estado()

        self.lift()
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self._guardar_y_salir)

    def _crear_interfaz(self):
        # Frame principal
        main = tk.Frame(self, bg="#f0f0f0", padx=15, pady=15)
        main.pack(fill="both", expand=True)

        # Título
        tk.Label(main, text="CAJA", 
                font=("Arial", 20, "bold"),
                bg="#f0f0f0", fg="#2c3e50").pack(pady=(0, 5))
        
        tk.Label(main, text="Gestión de Efectivo", 
                font=("Arial", 10),
                bg="#f0f0f0", fg="#666").pack(pady=(0, 15))

        # Estado de la caja
        self.estado_label = tk.Label(main, 
                                    text="🔒 CAJA CERRADA",
                                    font=("Arial", 12, "bold"),
                                    bg="#e74c3c", fg="white",
                                    padx=15, pady=10,
                                    relief="solid", bd=1)
        self.estado_label.pack(fill="x", pady=(0, 20))

        # Frame para botones
        botones_frame = tk.Frame(main, bg="#f0f0f0")
        botones_frame.pack(fill="both", expand=True)

        # Botones estilo checklist
        botones = [
            ("📄 Facturar", self.accion_facturar),
            ("📂 Apertura", self.accion_apertura),
            ("💸 Retiro", lambda: self._popup_operacion("Retiro de Caja", "retiro")),
            ("📋 Gastos", lambda: self._popup_operacion("Registrar Gasto", "gasto")),
            ("💳 Ingreso", lambda: self._popup_operacion("Ingreso de Caja", "ingreso")),
            ("🔒 Cierre Caja", self.accion_cierre),
            ("🚪 Salir", self._guardar_y_salir)
        ]

        for i, (texto, comando) in enumerate(botones):
            btn_frame = tk.Frame(botones_frame, bg="#f0f0f0")
            btn_frame.pack(fill="x", pady=3)
            
            # Simular checkbox con texto
            btn = tk.Label(btn_frame, text=f"□ {texto}", 
                          font=("Arial", 11),
                          bg="#f8f9fa", fg="#2c3e50",
                          padx=15, pady=10,
                          relief="solid", bd=1,
                          cursor="hand2")
            btn.pack(fill="x")
            
            # Bind clicks
            btn.bind("<Button-1>", lambda e, cmd=comando: cmd())
            
            # Efecto hover
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#e9ecef"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#f8f9fa"))

    def _actualizar_estado(self):
        if self.monto_apertura is not None:
            saldo_formateado = f"{self.saldo_sistema:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            self.estado_label.config(
                text=f"✅ CAJA ABIERTA - ${saldo_formateado}",
                bg="#27ae60"
            )
            # Marcar apertura como "checked"
            self._marcar_boton_como_activado(1)
        else:
            self.estado_label.config(
                text="🔒 CAJA CERRADA",
                bg="#e74c3c"
            )
            # Marcar apertura como "unchecked"
            self._marcar_boton_como_desactivado(1)

    def _marcar_boton_como_activado(self, indice):
        """Cambia el símbolo de □ a ✓ para indicar activado"""
        botones_frame = self.winfo_children()[0].winfo_children()[2]  # Frame de botones
        if indice < len(botones_frame.winfo_children()):
            btn = botones_frame.winfo_children()[indice].winfo_children()[0]
            texto_actual = btn.cget("text")
            nuevo_texto = texto_actual.replace("□", "✓")
            btn.config(text=nuevo_texto, fg="#27ae60")

    def _marcar_boton_como_desactivado(self, indice):
        """Cambia el símbolo de ✓ a □ para indicar desactivado"""
        botones_frame = self.winfo_children()[0].winfo_children()[2]  # Frame de botones
        if indice < len(botones_frame.winfo_children()):
            btn = botones_frame.winfo_children()[indice].winfo_children()[0]
            texto_actual = btn.cget("text")
            nuevo_texto = texto_actual.replace("✓", "□")
            btn.config(text=nuevo_texto, fg="#2c3e50")

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

    def accion_apertura(self):
        if self.monto_apertura is not None:
            messagebox.showerror("Error", "La caja ya está abierta.")
            return
        VentanaEmergenteCaja(self, "Apertura de Caja", "apertura", self.success_color, self._set_apertura)

    def _set_apertura(self, monto, motivo):
        self.monto_apertura = monto
        self.saldo_sistema = monto
        self.ventas_realizadas = []
        self._actualizar_estado()
        self._guardar_estado()

    def _popup_operacion(self, titulo, tipo):
        if not self.monto_apertura:
            messagebox.showerror("Error", "Debe abrir la caja primero.")
            return
        
        colores = {
            "retiro": "#e67e22",
            "gasto": "#e74c3c", 
            "ingreso": "#3498db"
        }
        VentanaEmergenteCaja(self, titulo, tipo, colores.get(tipo, "#3498db"))

    def accion_cierre(self):
        if not self.monto_apertura:
            messagebox.showerror("Error", "Debe abrir la caja para cerrarla.")
            return
        ventana_cierre_caja(self)

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

if __name__ == "__main__":
    app = CajaApp()
    app.mainloop()