import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import csv, os
from ventana import POSWindow

class CajaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("💰 Gestión de Caja")
        self.monto_apertura = None
        self.ventas_realizadas = []

        # Configuración de estilo naranja pastel
        self.bg_color = "#FFE5B4"  # Naranja pastel suave
        self.card_color = "#FFFFFF"  # Blanco para cards
        self.accent_color = "#FFB347"  # Naranja más fuerte
        self.text_color = "#2c3e50"  # Texto oscuro para contraste
        self.success_color = "#27ae60"  # Verde para acciones positivas
        self.danger_color = "#e74c3c"  # Rojo para acciones de riesgo

        # Configurar ventana
        ancho_ventana = 320
        alto_ventana = 580
        pantalla_alto = self.winfo_screenheight()
        y = (pantalla_alto - alto_ventana) // 2
        self.geometry(f"{ancho_ventana}x{alto_ventana}+50+{y - 150}")
        self.resizable(False, False)
        self.configure(bg=self.bg_color)

        # Configurar estilo ttk
        self.configurar_estilo()

        # Frame principal con padding
        main_frame = tk.Frame(self, bg=self.bg_color, padx=15, pady=15)
        main_frame.pack(fill="both", expand=True)

        # Título
        titulo_frame = tk.Frame(main_frame, bg=self.bg_color)
        titulo_frame.pack(fill="x", pady=(0, 20))

        tk.Label(titulo_frame, text="💰 CAJA", 
                font=("Arial", 20, "bold"), 
                bg=self.bg_color, fg=self.text_color).pack()
        
        tk.Label(titulo_frame, text="Gestión de Efectivo", 
                font=("Arial", 11), 
                bg=self.bg_color, fg=self.text_color).pack()

        # Estado de caja
        self.estado_frame = tk.Frame(main_frame, bg=self.card_color, relief="flat", bd=1)
        self.estado_frame.pack(fill="x", pady=(0, 15))

        self.estado_label = tk.Label(self.estado_frame, 
                                   text="🔒 CAJA CERRADA", 
                                   font=("Arial", 12, "bold"), 
                                   bg=self.danger_color, fg="white",
                                   padx=10, pady=8)
        self.estado_label.pack(fill="x")

        # Frame para botones con scroll si es necesario
        self.botones_frame = tk.Frame(main_frame, bg=self.bg_color)
        self.botones_frame.pack(fill="both", expand=True)

        self.crear_botones()

    def configurar_estilo(self):
        """Configura el estilo minimalista para los widgets"""
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except Exception:
            pass
        
        # Configurar estilo de botones
        style.configure('Caja.TButton',
                       font=('Arial', 11, 'bold'),
                       padding=(10, 8),
                       relief='flat',
                       background=self.accent_color,
                       foreground='white',
                       focuscolor='none')
        
        style.map('Caja.TButton',
                 background=[('active', self.accent_color),
                           ('pressed', self.accent_color)],
                 relief=[('pressed', 'sunken'),
                        ('active', 'raised')])

    def crear_botones(self):
        botones = [
            ("📄 Facturar", self.accion_facturar, self.accent_color),
            ("📂 Apertura", self.accion_apertura, self.success_color),
            ("💸 Retiro", self.accion_retiro, "#e67e22"),
            ("📋 Gastos", self.accion_gastos, "#e74c3c"),
            ("💳 Ingreso", self.accion_ingreso, "#3498db"),
            ("🔒 Cierre Caja", self.accion_cierre, "#9b59b6"),
            ("🖨️ Imprimir", self.accion_impresora, "#34495e"),
            ("🚪 Salir", self.accion_salir, "#95a5a6")
        ]

        for texto, comando, color in botones:
            # Frame para cada botón con espaciado
            btn_frame = tk.Frame(self.botones_frame, bg=self.bg_color, height=60)
            btn_frame.pack(fill="x", pady=4)
            btn_frame.pack_propagate(False)

            btn = tk.Button(btn_frame, text=texto, command=comando,
                          font=("Arial", 11, "bold"),
                          bg=color, fg="white",
                          relief="flat", bd=0,
                          cursor="hand2",
                          padx=15, pady=12,
                          anchor="w")
            btn.pack(fill="both", expand=True, padx=2)

            # Efecto hover
            def on_enter(e, btn=btn, color=color):
                btn.configure(bg=self.oscurecer_color(color, 20))
            
            def on_leave(e, btn=btn, color=color):
                btn.configure(bg=color)
            
            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

    def oscurecer_color(self, color, amount):
        """Oscurece un color hexadecimal"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        new_rgb = tuple(max(0, min(255, c - amount)) for c in rgb)
        return f'#{new_rgb[0]:02x}{new_rgb[1]:02x}{new_rgb[2]:02x}'

    def actualizar_estado_caja(self):
        """Actualiza el indicador de estado de la caja"""
        if self.monto_apertura is not None:
            self.estado_label.configure(
                text=f"✅ CAJA ABIERTA - ${self.monto_apertura:.2f}",
                bg=self.success_color
            )
        else:
            self.estado_label.configure(
                text="🔒 CAJA CERRADA",
                bg=self.danger_color
            )

    def accion_facturar(self):
        if self.monto_apertura is None:
            messagebox.showerror("Error", "Para facturar la caja debe estar abierta.")
            return
        
        ventana_factura = POSWindow(caja=self)
        ventana_factura.grab_set()
        ancho = 1000
        alto = 650
        x = 350
        y = (ventana_factura.winfo_screenheight() - alto) // 2
        ventana_factura.geometry(f"{ancho}x{alto}+{x}+{y}")

    def accion_apertura(self):
        if self.monto_apertura is not None:
            messagebox.showerror("Error", "La caja ya está abierta.")
            return

        popup = tk.Toplevel(self)
        popup.title("Apertura de Caja")
        popup.geometry("300x200")
        popup.transient(self)
        popup.grab_set()
        popup.configure(bg=self.bg_color)

        # Centrar ventana
        x = (self.winfo_screenwidth() - 300) // 2
        y = (self.winfo_screenheight() - 200) // 2
        popup.geometry(f"+{x}+{y}")

        # Contenido del popup
        content_frame = tk.Frame(popup, bg=self.card_color, padx=20, pady=20, relief="flat", bd=1)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(content_frame, text="💰 APERTURA DE CAJA", 
                font=("Arial", 14, "bold"), 
                bg=self.card_color, fg=self.text_color).pack(pady=(0, 15))

        tk.Label(content_frame, text="Efectivo inicial:", 
                font=("Arial", 11), 
                bg=self.card_color, fg=self.text_color).pack(anchor="w")

        efectivo_entry = tk.Entry(content_frame, font=("Arial", 12), 
                                justify="center", relief="solid", bd=1)
        efectivo_entry.pack(fill="x", pady=10, ipady=5)
        efectivo_entry.focus()

        def aceptar():
            texto = efectivo_entry.get().strip()
            texto = texto.replace(".", "").replace(",", ".")
            if not texto.replace(".", "", 1).isdigit():
                messagebox.showerror("Error", "Ingrese un monto válido.")
                return
            self.monto_apertura = float(texto)
            self.actualizar_estado_caja()
            messagebox.showinfo("Éxito", f"Apertura registrada con ${self.monto_apertura:.2f}")
            popup.destroy()

        def cancelar():
            popup.destroy()

        # Frame para botones
        frame_botones = tk.Frame(content_frame, bg=self.card_color)
        frame_botones.pack(fill="x", pady=(10, 0))

        tk.Button(frame_botones, text="Aceptar", command=aceptar,
                 bg=self.success_color, fg="white", font=("Arial", 10, "bold"),
                 relief="flat", padx=20, pady=8).pack(side="right", padx=5)

        tk.Button(frame_botones, text="Cancelar", command=cancelar,
                 bg=self.danger_color, fg="white", font=("Arial", 10),
                 relief="flat", padx=20, pady=8).pack(side="right", padx=5)

        popup.bind('<Return>', lambda e: aceptar())
        popup.bind('<Escape>', lambda e: cancelar())

    def accion_retiro(self):
        if self.monto_apertura is None:
            messagebox.showerror("Error", "La caja debe estar abierta para realizar un retiro.")
            return

        self._mostrar_popup_operacion("Retiro de Caja", "retiro", "#e67e22")

    def accion_gastos(self):
        if self.monto_apertura is None:
            messagebox.showerror("Error", "La caja debe estar abierta para registrar un gasto")
            return
        
        self._mostrar_popup_operacion("Registrar Gasto", "gasto", "#e74c3c")

    def _mostrar_popup_operacion(self, titulo, tipo, color):
        popup = tk.Toplevel(self)
        popup.title(titulo)
        popup.geometry("350x280")
        popup.transient(self)
        popup.grab_set()
        popup.configure(bg=self.bg_color)

        x = (self.winfo_screenwidth() - 350) // 2
        y = (self.winfo_screenheight() - 280) // 2
        popup.geometry(f"+{x}+{y}")

        # Contenido
        content_frame = tk.Frame(popup, bg=self.card_color, padx=20, pady=20, relief="flat", bd=1)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(content_frame, text=f"💰 {titulo.upper()}", 
                font=("Arial", 14, "bold"), 
                bg=self.card_color, fg=self.text_color).pack(pady=(0, 10))

        # Saldo disponible
        monto_formateado = f"{self.monto_apertura:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        saldo_frame = tk.Frame(content_frame, bg="#f8f9fa", relief="solid", bd=1, padx=10, pady=8)
        saldo_frame.pack(fill="x", pady=5)
        
        tk.Label(saldo_frame, text=f"Saldo disponible: ${monto_formateado}", 
                font=("Arial", 10, "bold"), 
                bg="#f8f9fa", fg=self.text_color).pack()

        # Campos del formulario
        campos_frame = tk.Frame(content_frame, bg=self.card_color)
        campos_frame.pack(fill="x", pady=15)

        tk.Label(campos_frame, text=f"Motivo del {tipo}:", 
                font=("Arial", 10), 
                bg=self.card_color, fg=self.text_color).pack(anchor="w")
        
        motivo_entry = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        motivo_entry.pack(fill="x", pady=(5, 10), ipady=3)

        tk.Label(campos_frame, text=f"Monto a {tipo}:", 
                font=("Arial", 10), 
                bg=self.card_color, fg=self.text_color).pack(anchor="w")
        
        monto_entry = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        monto_entry.pack(fill="x", pady=(5, 0), ipady=3)
        monto_entry.focus()

        def aceptar():
            motivo = motivo_entry.get().strip()
            texto_monto = monto_entry.get().strip().replace(".", "").replace(",", ".")
            if not texto_monto.replace(".", "", 1).isdigit():
                messagebox.showerror("Error", "Ingrese un monto válido.")
                return

            monto_operacion = float(texto_monto)
            if monto_operacion > self.monto_apertura:
                messagebox.showerror("Error", "El monto excede el saldo disponible.")
                return

            self.monto_apertura -= monto_operacion
            self.actualizar_estado_caja()
            
            if tipo == "retiro":
                messagebox.showinfo("Éxito", f"✅ Retiro realizado\n${monto_operacion:.2f}\nMotivo: {motivo}")
            else:
                messagebox.showinfo("Éxito", f"✅ Gasto registrado\n${monto_operacion:.2f}\nMotivo: {motivo}")
            
            popup.destroy()

        def cancelar():
            popup.destroy()

        # Botones
        frame_botones = tk.Frame(content_frame, bg=self.card_color)
        frame_botones.pack(fill="x", pady=(10, 0))

        tk.Button(frame_botones, text="Aceptar", command=aceptar,
                 bg=color, fg="white", font=("Arial", 10, "bold"),
                 relief="flat", padx=20, pady=8).pack(side="right", padx=5)

        tk.Button(frame_botones, text="Cancelar", command=cancelar,
                 bg=self.danger_color, fg="white", font=("Arial", 10),
                 relief="flat", padx=20, pady=8).pack(side="right", padx=5)

        popup.bind('<Return>', lambda e: aceptar())
        popup.bind('<Escape>', lambda e: cancelar())

    def accion_ingreso(self):
        if self.monto_apertura is None:
            messagebox.showerror("Error", "La caja debe estar abierta para realizar un ingreso.")
            return

        self._mostrar_popup_ingreso()

    def _mostrar_popup_ingreso(self):
        popup = tk.Toplevel(self)
        popup.title("Ingreso de Caja")
        popup.geometry("350x250")
        popup.transient(self)
        popup.grab_set()
        popup.configure(bg=self.bg_color)

        x = (self.winfo_screenwidth() - 350) // 2
        y = (self.winfo_screenheight() - 250) // 2
        popup.geometry(f"+{x}+{y}")

        # Contenido
        content_frame = tk.Frame(popup, bg=self.card_color, padx=20, pady=20, relief="flat", bd=1)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(content_frame, text="💳 INGRESO DE CAJA", 
                font=("Arial", 14, "bold"), 
                bg=self.card_color, fg=self.text_color).pack(pady=(0, 10))

        # Saldo actual
        monto_formateado = f"{self.monto_apertura:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        saldo_frame = tk.Frame(content_frame, bg="#f8f9fa", relief="solid", bd=1, padx=10, pady=8)
        saldo_frame.pack(fill="x", pady=5)
        
        tk.Label(saldo_frame, text=f"Saldo actual: ${monto_formateado}", 
                font=("Arial", 10, "bold"), 
                bg="#f8f9fa", fg=self.text_color).pack()

        # Campos
        campos_frame = tk.Frame(content_frame, bg=self.card_color)
        campos_frame.pack(fill="x", pady=15)

        tk.Label(campos_frame, text="Motivo del ingreso:", 
                font=("Arial", 10), 
                bg=self.card_color, fg=self.text_color).pack(anchor="w")
        
        motivo_entry = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        motivo_entry.pack(fill="x", pady=(5, 10), ipady=3)

        tk.Label(campos_frame, text="Monto a ingresar:", 
                font=("Arial", 10), 
                bg=self.card_color, fg=self.text_color).pack(anchor="w")
        
        monto_entry = tk.Entry(campos_frame, font=("Arial", 10), relief="solid", bd=1)
        monto_entry.pack(fill="x", pady=(5, 0), ipady=3)
        monto_entry.focus()

        def aceptar():
            motivo = motivo_entry.get().strip()
            texto_monto = monto_entry.get().strip().replace(".", "").replace(",", ".")
            if not texto_monto.replace(".", "", 1).isdigit():
                messagebox.showerror("Error", "Ingrese un monto válido.")
                return
            monto_ingreso = float(texto_monto)
            self.monto_apertura += monto_ingreso
            self.actualizar_estado_caja()
            messagebox.showinfo("Éxito", f"✅ Ingreso realizado\n${monto_ingreso:.2f}\nMotivo: {motivo}")
            popup.destroy()

        def cancelar():
            popup.destroy()

        # Botones
        frame_botones = tk.Frame(content_frame, bg=self.card_color)
        frame_botones.pack(fill="x", pady=(10, 0))

        tk.Button(frame_botones, text="Aceptar", command=aceptar,
                 bg=self.success_color, fg="white", font=("Arial", 10, "bold"),
                 relief="flat", padx=20, pady=8).pack(side="right", padx=5)

        tk.Button(frame_botones, text="Cancelar", command=cancelar,
                 bg=self.danger_color, fg="white", font=("Arial", 10),
                 relief="flat", padx=20, pady=8).pack(side="right", padx=5)

        popup.bind('<Return>', lambda e: aceptar())
        popup.bind('<Escape>', lambda e: cancelar())

    # ------------------ CIERRE DE CAJA NUEVO ------------------
    def accion_cierre(self):
        if self.monto_apertura is None:
            messagebox.showerror("Error", "La caja tiene que estar abierta para poder cerrarla.")
            return

        popup = tk.Toplevel(self)
        popup.title("🔒 Cierre de Caja")
        popup.geometry("600x500")
        popup.transient(self)
        popup.grab_set()
        popup.configure(bg=self.bg_color)

        x = (self.winfo_screenwidth() - 600) // 2
        y = (self.winfo_screenheight() - 500) // 2
        popup.geometry(f"+{x}+{y}")

        # FRAME PRINCIPAL
        content_frame = tk.Frame(popup, bg=self.card_color, padx=20, pady=20, relief="flat", bd=1)
        content_frame.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(content_frame, text="🧾 CIERRE DE CAJA", font=("Arial", 16, "bold"),
                 bg=self.card_color, fg=self.text_color).pack(pady=(0, 15))

        # Obtener saldo de sistema (simulación desde ventas.csv)
        self.saldo_sistema = self._obtener_saldo_sistema()

        # SALDO DEL SISTEMA
        frame_datos = tk.Frame(content_frame, bg=self.card_color)
        frame_datos.pack(pady=5, fill="x")

        tk.Label(frame_datos, text="💻 Saldo del Sistema:", font=("Arial", 11, "bold"),
                 bg=self.card_color, fg=self.text_color).grid(row=0, column=0, sticky="w")
        self.lbl_sistema = tk.Label(frame_datos, text=f"${self.saldo_sistema:.2f}",
                                   font=("Arial", 11), bg=self.card_color, fg=self.text_color)
        self.lbl_sistema.grid(row=0, column=1, sticky="e", padx=20)

        # IMPORTE EN CAJA
        tk.Label(frame_datos, text="💵 Importe en Caja:", font=("Arial", 11, "bold"),
                 bg=self.card_color, fg=self.text_color).grid(row=1, column=0, sticky="w", pady=10)
        self.entry_caja = tk.Entry(frame_datos, font=("Arial", 11), justify="center", relief="solid", bd=1)
        self.entry_caja.grid(row=1, column=1, sticky="e", padx=20)

        # IMPORTE EN TRANSFERENCIA
        tk.Label(frame_datos, text="🏦 Importe en Transferencia:", font=("Arial", 11, "bold"),
                 bg=self.card_color, fg=self.text_color).grid(row=2, column=0, sticky="w", pady=10)
        self.entry_transf = tk.Entry(frame_datos, font=("Arial", 11), justify="center", relief="solid", bd=1)
        self.entry_transf.grid(row=2, column=1, sticky="e", padx=20)

        # DIFERENCIA
        tk.Label(frame_datos, text="📊 Diferencia de Caja:", font=("Arial", 12, "bold"),
                 bg=self.card_color, fg=self.text_color).grid(row=3, column=0, sticky="w", pady=15)
        self.lbl_diferencia = tk.Label(frame_datos, text="$ 0.00",
                                      font=("Arial", 16, "bold"),
                                      bg=self.card_color, fg=self.danger_color)
        self.lbl_diferencia.grid(row=3, column=1, sticky="e", padx=20)

        # BOTONES
        btn_frame = tk.Frame(content_frame, bg=self.card_color)
        btn_frame.pack(pady=25, fill="x")

        tk.Button(btn_frame, text="💰 Calcular Diferencia", bg=self.success_color,
                  fg="white", font=("Arial", 11, "bold"), relief="flat",
                  padx=15, pady=10, command=self._calcular_diferencia).pack(side="left", padx=10)

        tk.Button(btn_frame, text="✅ Confirmar Cierre", bg="#f39c12",
                  fg="white", font=("Arial", 11, "bold"), relief="flat",
                  padx=15, pady=10, command=lambda: self.finalizar_caja(popup)).pack(side="right", padx=10)

        tk.Button(btn_frame, text="❌ Cancelar", bg=self.danger_color,
                  fg="white", font=("Arial", 10), relief="flat",
                  padx=15, pady=10, command=popup.destroy).pack(side="right", padx=5)

    def _obtener_saldo_sistema(self):
        """Suma todas las ventas registradas desde ventas.csv"""
        total = 0
        ruta = os.path.join("data", "ventas", "ventas.csv")
        if os.path.isfile(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)
                for fila in reader:
                    try:
                        total += float(fila[2])
                    except Exception:
                        pass
        return total

    def _calcular_diferencia(self):
        """Calcula diferencia entre importes ingresados y saldo sistema"""
        try:
            efectivo = float(self.entry_caja.get() or 0)
            transferencia = float(self.entry_transf.get() or 0)
            diferencia = (efectivo + transferencia) - self.saldo_sistema
            color = self.success_color if abs(diferencia) < 0.005 else self.danger_color
            self.lbl_diferencia.config(text=f"${diferencia:.2f}", fg=color)
        except Exception:
            messagebox.showerror("Error", "Ingrese montos válidos.")

    def finalizar_caja(self, ventana):
        """Finaliza el cierre: guarda un registro y resetea el estado de caja."""
        try:
            efectivo = float(self.entry_caja.get() or 0)
            transferencia = float(self.entry_transf.get() or 0)
        except Exception:
            messagebox.showerror("Error", "Ingrese montos válidos.")
            return

        diferencia = (efectivo + transferencia) - self.saldo_sistema

        # Guardar en CSV
        try:
            os.makedirs("data/cierres", exist_ok=True)
            ruta = os.path.join("data/cierres", "cierres.csv")
            existe = os.path.isfile(ruta)
            with open(ruta, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if not existe:
                    writer.writerow(["Fecha", "Saldo Sistema", "Efectivo", "Transferencia", "Diferencia"])
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    f"{self.saldo_sistema:.2f}",
                    f"{efectivo:.2f}",
                    f"{transferencia:.2f}",
                    f"{diferencia:.2f}"
                ])
        except Exception as err:
            messagebox.showerror("Error", f"No se pudo guardar el cierre:\n{err}")
            return

        messagebox.showinfo("Cierre de Caja", "✅ Caja cerrada correctamente")
        self.monto_apertura = None
        self.actualizar_estado_caja()
        ventana.destroy()

    def accion_impresora(self):
        messagebox.showinfo("Impresora", "🖨️ Función de impresión activada")

    def accion_salir(self):
        if messagebox.askyesno("Salir", "¿Está seguro que desea cerrar la gestión de caja?"):
            self.destroy()

if __name__ == "__main__":
    app = CajaApp()
    app.mainloop()
