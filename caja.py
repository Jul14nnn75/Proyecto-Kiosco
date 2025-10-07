import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class CajaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menu Caja")
        self.monto_apertura = None  # La caja está cerrada por defecto

        # Posicionar ventana a la izquierda y centrada verticalmente
        ancho_ventana = 300
        alto_ventana = 550
        pantalla_alto = self.winfo_screenheight()
        y = (pantalla_alto - alto_ventana) // 2
        self.geometry(f"{ancho_ventana}x{alto_ventana}+0+{y - 150}")
        self.resizable(False,False)

        self.config(padx=20, pady=20)
        self.crear_botones()

    def crear_botones(self):
        botones = [
            ("Facturar", self.accion_facturar),
            ("Apertura", self.accion_apertura),
            ("Retiro", self.accion_retiro),
            ("Gastos", self.accion_gastos),
            ("Ingreso", self.accion_ingreso),
            ("Cierre Caja", self.accion_cierre),
            ("Imprimir", self.accion_impresora),
            (" Salir", self.accion_salir)
        ]

        for texto, comando in botones:
            boton = ttk.Button(self, text=texto, command=comando)
            boton.pack(fill="x", pady=10, ipady=10)

    def accion_facturar(self):
        if self.monto_apertura is None:
            messagebox.showerror("Error", "Para facturar la caja debe estar abierta.")
            return
        print("Caja abierta, listo para facturar.")

    def accion_apertura(self):
        if self.monto_apertura is not None:
            messagebox.showerror("Error", "La caja ya está abierta.")
            return

        popup = tk.Toplevel(self)
        popup.title("Apertura de Caja")
        popup.geometry("250x150")
        popup.transient(self)
        popup.grab_set()

        x = (self.winfo_screenwidth() - 250) // 2
        y = (self.winfo_screenheight() - 150) // 2
        popup.geometry(f"+{x}+{y}")

        ttk.Label(popup, text="EFECTIVO").pack(pady=(15, 5))
        efectivo_entry = ttk.Entry(popup)
        efectivo_entry.pack(pady=5)

        def aceptar():
            texto = efectivo_entry.get().strip()
            texto = texto.replace(".", "").replace(",", ".")
            if not texto.replace(".", "", 1).isdigit():
                messagebox.showerror("Error", "Ingrese un monto válido.")
                return
            self.monto_apertura = float(texto)
            print(f"Apertura registrada con ${self.monto_apertura}")
            popup.destroy()

        def cancelar():
            popup.destroy()

        frame_botones = ttk.Frame(popup)
        frame_botones.pack(pady=10)

        ttk.Button(frame_botones, text="Aceptar", command=aceptar).pack(side="left", padx=10)
        ttk.Button(frame_botones, text="Cancelar", command=cancelar).pack(side="left", padx=10)

    def accion_retiro(self):
        if self.monto_apertura is None:
            messagebox.showerror("Error", "La caja debe estar abierta para realizar un retiro.")
            return

        popup = tk.Toplevel(self)
        popup.title("Retiro de Caja")
        popup.geometry("300x220")
        popup.transient(self)
        popup.grab_set()

        x = (self.winfo_screenwidth() - 300) // 2
        y = (self.winfo_screenheight() - 220) // 2
        popup.geometry(f"+{x}+{y}")

        monto_formateado = f"{int(self.monto_apertura):,}".replace(",", ".")
        saldo_label = ttk.Label(popup, text=f"Saldo disponible: ${monto_formateado}")
        saldo_label.pack(pady=(15, 5))

        ttk.Label(popup, text="Motivo del retiro:").pack()
        motivo_entry = ttk.Entry(popup)
        motivo_entry.pack(pady=5)

        ttk.Label(popup, text="Monto a retirar:").pack()
        monto_entry = ttk.Entry(popup)
        monto_entry.pack(pady=5)

        def aceptar():
            motivo = motivo_entry.get().strip()
            texto_monto = monto_entry.get().strip().replace(".", "").replace(",", ".")
            if not texto_monto.replace(".", "", 1).isdigit():
                messagebox.showerror("Error", "Ingrese un monto válido.")
                return

            monto_retiro = float(texto_monto)
            if monto_retiro > self.monto_apertura:
                messagebox.showerror("Error", "El monto excede el saldo disponible.")
                return

            self.monto_apertura -= monto_retiro
            print(f"Retiro realizado: ${monto_retiro:.2f} | Motivo: {motivo}")
            popup.destroy()

        def cancelar():
            popup.destroy()

        frame_botones = ttk.Frame(popup)
        frame_botones.pack(pady=10)

        ttk.Button(frame_botones, text="Aceptar", command=aceptar).pack(side="left", padx=10)
        ttk.Button(frame_botones, text="Cancelar", command=cancelar).pack(side="left", padx=10)

    def accion_gastos(self):
        if self.monto_apertura is None:
            messagebox.showerror("Error","Lac caja debe estar abierta para registrar un gasto")
            return
        
        popup = tk.Toplevel(self)
        popup.title("Registrar Gasto")
        popup.geometry("300x220")
        popup.transient(self)
        popup.grab_set()

        x = (self.winfo_screenwidth() - 300) // 2
        y = (self.winfo_screenheight() - 220) // 2
        popup.geometry(f"+{x}+{y}")

        monto_formateado = f"{int(self.monto_apertura):,}".replace(",", ".")
        saldo_label = ttk.Label(popup, text=f"Saldo disponible: ${monto_formateado}")
        saldo_label.pack(pady=(15, 5))

        ttk.Label(popup, text="Motivo del gasto:").pack()
        motivo_entry = ttk.Entry(popup)
        motivo_entry.pack(pady=5)

        ttk.Label(popup, text="Importe Gasto:").pack()
        monto_entry = ttk.Entry(popup)
        monto_entry.pack(pady=5)

        def aceptar():
            motivo = motivo_entry.get().strip()
            texto_monto = monto_entry.get().strip().replace(".","").replace(",", ".")
            if not texto_monto.replace(".","",1).isdigit():
                messagebox.showerror("Error","Ingrese un monto valido.")
                return
            
            monto_gasto = float(texto_monto)
            if monto_gasto > self.monto_apertura:
                messagebox.showerror("Error","El gasto excede el saldo disponible.")
                return
            
            self.monto_apertura -= monto_gasto
            print(f"Gasto registrado: ${monto_gasto:.2f} | Motivo: {motivo}")
            popup.destroy()
        
        def cancelar():
            popup.destroy()

        frame_botones = ttk.Frame(popup)
        frame_botones.pack(pady=10)

        ttk.Button(frame_botones,text="Aceptar",command=aceptar).pack(side="left",padx=10)
        ttk.Button(frame_botones,text="Cancelar",command=cancelar).pack(side="left",padx=10)


    def accion_ingreso(self):
        if self.monto_apertura is None:
            messagebox.showerror("Error", "La caja debe estar abierta para realizar un ingreso.")
            return

        popup = tk.Toplevel(self)
        popup.title("Ingreso de Caja")
        popup.geometry("300x220")
        popup.transient(self)
        popup.grab_set()

        x = (self.winfo_screenwidth() - 300) // 2
        y = (self.winfo_screenheight() - 220) // 2
        popup.geometry(f"+{x}+{y}")

        monto_formateado = f"{int(self.monto_apertura):,}".replace(",", ".")
        saldo_label = ttk.Label(popup, text=f"Saldo disponible: ${monto_formateado}")
        saldo_label.pack(pady=(15, 5))

        ttk.Label(popup, text="Motivo del ingreso:").pack()
        motivo_entry = ttk.Entry(popup)
        motivo_entry.pack(pady=5)

        ttk.Label(popup, text="Monto a ingresar:").pack()
        monto_entry = ttk.Entry(popup)
        monto_entry.pack(pady=5)

        def aceptar():
            motivo = motivo_entry.get().strip()
            texto_monto = monto_entry.get().strip().replace(".", "").replace(",", ".")
            if not texto_monto.replace(".", "", 1).isdigit():
                messagebox.showerror("Error", "Ingrese un monto válido.")
                return
            monto_ingreso = float(texto_monto)
            self.monto_apertura += monto_ingreso
            print(f"Ingreso realizado: ${monto_ingreso:.2f} | Motivo: {motivo}")
            popup.destroy()

        def cancelar():
            popup.destroy()

        frame_botones = ttk.Frame(popup)
        frame_botones.pack(pady=10)

        ttk.Button(frame_botones, text="Aceptar", command=aceptar).pack(side="left", padx=10)
        ttk.Button(frame_botones, text="Cancelar", command=cancelar).pack(side="left", padx=10)

    def accion_cierre(self):
        if self.monto_apertura is None:
            messagebox.showerror("Error", "La caja ya está cerrada.")
            return

        ahora = datetime.now()
        fecha = ahora.strftime("%d/%m/%Y")
        hora = ahora.strftime("%H:%M:%S")

        monto_formateado = f"{int(self.monto_apertura):,}".replace(",", ".")

        mensaje = (
            f"Caja cerrada correctamente.\n"
            f"Fecha: {fecha}\n"
            f"Hora: {hora}\n"
            f"Monto final: ${monto_formateado}"
        )
        messagebox.showinfo("Cierre de Caja", mensaje)
        self.monto_apertura = None

    def accion_impresora(self):
        print("Impresora presionado")

    def accion_salir(self):
        print("Cerrando app...")
        self.destroy()

if __name__ == "__main__":
    app = CajaApp()
    app.mainloop()
