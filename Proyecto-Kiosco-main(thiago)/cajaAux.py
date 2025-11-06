import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Alignment, PatternFill

# -----------------------------------------
# 🔸 POPUP REUTILIZABLE: Apertura / Retiro / Ingreso / Gasto
# -----------------------------------------
class CajaPopup(tk.Toplevel):
    def __init__(self, master, titulo, tipo, color, callback=None):
        super().__init__(master)
        self.title(titulo)
        self.geometry("400x300")
        self.transient(master)
        self.grab_set()
        self.configure(bg=master.bg_color)
        self.callback = callback
        self.tipo = tipo
        self.master = master
        self.color = color

        self.centrar_ventana(400, 300)

        frame = tk.Frame(self, bg=master.card_color, padx=20, pady=20)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(frame, text=f"💰 {titulo.upper()}",
                 font=("Arial", 16, "bold"),
                 bg=master.card_color, fg=master.text_color).pack(pady=(0, 15))

        if tipo not in ("apertura", "gasto"):
            saldo = f"{master.saldo_sistema:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            sf = tk.Frame(frame, bg="#f8f9fa", relief="solid", bd=1, padx=10, pady=6)
            sf.pack(fill="x", pady=(0, 15))
            tk.Label(sf, text=f"Saldo actual: ${saldo}", font=("Arial", 11, "bold"),
                     bg="#f8f9fa", fg=master.text_color).pack()

        campos = tk.Frame(frame, bg=master.card_color)
        campos.pack(fill="x", pady=10)

        if tipo != "apertura":
            tk.Label(campos, text=f"Motivo del {tipo}:", font=("Arial", 11),
                     bg=master.card_color, fg=master.text_color).pack(anchor="w")
            self.motivo_entry = tk.Entry(campos, font=("Arial", 12), relief="solid", bd=1)
            self.motivo_entry.pack(fill="x", pady=(5, 15), ipady=5)
        else:
            self.motivo_entry = None

        tk.Label(campos, text=f"Monto a {tipo}:", font=("Arial", 11),
                 bg=master.card_color, fg=master.text_color).pack(anchor="w")
        self.monto_entry = tk.Entry(campos, font=("Arial", 14, "bold"), relief="solid", bd=1, justify="center")
        self.monto_entry.pack(fill="x", pady=(5, 0), ipady=5)
        self.monto_entry.focus()

        botones = tk.Frame(frame, bg=master.card_color)
        botones.pack(fill="x", pady=(20, 0))

        tk.Button(botones, text="Aceptar", command=self.aceptar,
                  bg=color, fg="white", font=("Arial", 11, "bold"),
                  relief="flat", padx=20, pady=10).pack(side="right", padx=5)
        tk.Button(botones, text="Cancelar", command=self.destroy,
                  bg=master.danger_color, fg="white", font=("Arial", 11),
                  relief="flat", padx=20, pady=10).pack(side="right", padx=5)

        self.bind("<Return>", lambda e: self.aceptar())
        self.bind("<Escape>", lambda e: self.destroy())

    def centrar_ventana(self, ancho, alto):
        x = (self.winfo_screenwidth() - ancho) // 2
        y = (self.winfo_screenheight() - alto) // 2
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def aceptar(self):
        texto_monto = self.monto_entry.get().strip().replace(".", "").replace(",", ".")
        try:
            monto = float(texto_monto)
        except:
            messagebox.showerror("Error", "Ingrese un monto válido.")
            return

        motivo = self.motivo_entry.get().strip() if self.motivo_entry else "(Apertura)"

        if self.tipo == "ingreso":
            self.master.saldo_sistema += monto
            self.master.ingreso_actual = (motivo, monto)
        elif self.tipo == "retiro":
            if monto > self.master.saldo_sistema:
                messagebox.showerror("Error", "El monto excede el saldo disponible.")
                return
            self.master.saldo_sistema -= monto
            self.master.retiro_actual = (motivo, monto)
        elif self.tipo == "gasto":
            if not hasattr(self.master, "gastos"):
                self.master.gastos = []
            self.master.gastos.append((motivo, monto))
        elif self.tipo == "apertura":
            self.master.monto_apertura = monto
            self.master.saldo_sistema = monto

        if self.callback:
            self.callback(monto, motivo)

        self.master._actualizar_estado()
        self.master._guardar_estado()
        self.destroy()


# -----------------------------------------
# 🔒 POPUP DE CIERRE DE CAJA
# -----------------------------------------
def popup_cierre_caja(master):
    popup = tk.Toplevel(master)
    popup.title("🔒 Cierre de Caja")
    popup.geometry("500x500")
    popup.configure(bg=master.bg_color)
    popup.transient(master)
    popup.grab_set()
    popup.lift()
    popup.attributes("-topmost", True)

    frame = tk.Frame(popup, bg=master.card_color, padx=25, pady=25)
    frame.pack(fill="both", expand=True, padx=15, pady=15)

    tk.Label(frame, text="🧾 RESUMEN DE CAJA", font=("Arial", 15, "bold"),
             bg=master.card_color, fg=master.text_color).pack(pady=(0, 15))

    saldo_sistema = getattr(master, "saldo_sistema", 0.0)

    tk.Label(frame, text="💻 Saldo del Sistema:", font=("Arial", 11, "bold"),
             bg=master.card_color, fg=master.text_color).pack(anchor="w")
    tk.Label(frame, text=f"${saldo_sistema:.2f}", font=("Arial", 11),
             bg=master.card_color, fg=master.text_color).pack(anchor="w", pady=(0, 10))

    tk.Label(frame, text="💵 Importe de Caja:", font=("Arial", 11, "bold"),
             bg=master.card_color, fg=master.text_color).pack(anchor="w")
    entry_caja = tk.Entry(frame, font=("Arial", 12), relief="solid", bd=1)
    entry_caja.pack(fill="x", pady=(5, 10))

    tk.Label(frame, text="🏦 Importe Transferencia:", font=("Arial", 11, "bold"),
             bg=master.card_color, fg=master.text_color).pack(anchor="w")
    entry_transfer = tk.Entry(frame, font=("Arial", 12), relief="solid", bd=1)
    entry_transfer.pack(fill="x", pady=(5, 10))

    lbl_dif = tk.Label(frame, text="Diferencia: $0.00", font=("Arial", 12, "bold"),
                       bg=master.card_color, fg=master.text_color)
    lbl_dif.pack(pady=(10, 5))

    def calcular_dif(*args):
        try:
            caja = float(entry_caja.get().replace(",", ".") or 0)
            transfer = float(entry_transfer.get().replace(",", ".") or 0)
            dif = caja + transfer - saldo_sistema
            lbl_dif.config(text=f"Diferencia: ${dif:.2f}",
                           fg="green" if dif >= 0 else "red")
        except ValueError:
            lbl_dif.config(text="Diferencia: $0.00", fg="black")

    entry_caja.bind("<KeyRelease>", calcular_dif)
    entry_transfer.bind("<KeyRelease>", calcular_dif)

    botones = tk.Frame(frame, bg=master.card_color)
    botones.pack(fill="x", pady=(20, 0))

    tk.Button(botones, text="Aceptar", font=("Arial", 11, "bold"), bg="#27ae60", fg="white",
              command=lambda: confirmar_cierre(master, popup, entry_caja, entry_transfer)).pack(side="right", padx=5)
    tk.Button(botones, text="Cancelar", font=("Arial", 11), bg="#e74c3c", fg="white",
              command=popup.destroy).pack(side="right", padx=5)


def confirmar_cierre(master, popup, entry_caja, entry_transfer):
    try:
        caja = float(entry_caja.get().replace(",", ".") or 0)
        transfer = float(entry_transfer.get().replace(",", ".") or 0)
    except ValueError:
        messagebox.showerror("Error", "Ingrese valores numéricos válidos.")
        return

    saldo_sistema = getattr(master, "saldo_sistema", 0)
    diferencia = caja + transfer - saldo_sistema

    ingreso = getattr(master, "ingreso_actual", ("", 0))
    retiro = getattr(master, "retiro_actual", ("", 0))
    gastos = getattr(master, "gastos", [])

    guardar_cierre(saldo_sistema, caja, transfer, diferencia, ingreso, retiro, gastos)

    # Resetear todo
    master.monto_apertura = None
    master.saldo_sistema = 0
    master.ingreso_actual = ("", 0)
    master.retiro_actual = ("", 0)
    master.gastos = []
    master._actualizar_estado()
    master._guardar_estado()

    messagebox.showinfo("Cierre de Caja", "✅ Cierre guardado correctamente.")
    popup.destroy()


# -----------------------------------------
# 📊 GUARDAR CIERRE DE CAJA (Excel)
# -----------------------------------------
def guardar_cierre(saldo_sistema, importe_caja, importe_transfer, diferencia, ingreso, retiro, gastos):
    os.makedirs("data/cierres", exist_ok=True)
    ruta = os.path.join("data/cierres", "cierres.xlsx")

    if os.path.exists(ruta):
        wb = load_workbook(ruta)
        ws = wb.active
    else:
        wb = Workbook()
        ws = wb.active
        ws.title = "Resumen de Caja"

        ws.merge_cells("A1:L1")
        celda_titulo = ws["A1"]
        celda_titulo.value = "Resumen de Caja"
        celda_titulo.font = Font(size=16, bold=True, color="FFFFFF")
        celda_titulo.alignment = Alignment(horizontal="center", vertical="center")
        celda_titulo.fill = PatternFill(start_color="4CAF50", end_color="4CAF50", fill_type="solid")

        encabezados = [
            "Fecha", "Saldo Sistema", "Importe Caja", "Importe Transferencia", "Diferencia",
            "Motivo Ingreso", "Ingreso", "Motivo Retiro", "Retiro", "Motivo Gasto", "Gasto", "Gasto 2..."
        ]
        ws.append([""] * len(encabezados))
        ws.append(encabezados)
        for col in range(1, len(encabezados) + 1):
            ws.column_dimensions[chr(64 + col)].width = 20

    fila = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        f"{saldo_sistema:.2f}",
        f"{importe_caja:.2f}",
        f"{importe_transfer:.2f}",
        f"{diferencia:.2f}",
        ingreso[0], f"{ingreso[1]:.2f}",
        retiro[0], f"{retiro[1]:.2f}",
    ]

    # Agregar todos los gastos por separado
    for g in gastos:
        fila.extend([g[0], f"{g[1]:.2f}"])

    ws.append(fila)
    wb.save(ruta)
    print(f"✅ Cierre guardado en {ruta}")
