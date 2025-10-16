import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from mainFacturacion import POSWindow
class CajaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menu Caja")
        self.monto_apertura = None  # La caja está cerrada por defecto
        self.ventas_realizadas = []

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
        
        ventana_factura = POSWindow(caja=self)
        ventana_factura.grab_set()
        ancho = 1000
        alto = 650
        x = 320
        y = (ventana_factura.winfo_screenheight()- alto ) // 2
        ventana_factura.geometry(f"{ancho}x{alto}+{x}+{y}")
        

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
        
        popup = tk.Toplevel(self)
        popup.title("Cierre de Caja")
        popup.geometry("750x520")
        popup.transient(self)
        popup.grab_set()

        x = (self.winfo_screenwidth() - 750) // 2
        y = (self.winfo_screenheight() - 520) // 2
        popup.geometry(f"+{x}+{y}")

        #Creo pestañas

        notebook = ttk.Notebook(popup)
        notebook.pack(fill="both",expand=True,padx=10,pady=10)


        frame_efectivo = ttk.Frame(notebook)
        frame_tarjeta = ttk.Frame(notebook)
        notebook.add(frame_efectivo,text="1) Efectivo")
        notebook.add(frame_tarjeta,text="2) Tarjetas")
        

        #Apertura
        apertura_tree = ttk.Treeview(frame_efectivo,columns=("Fecha", "Descripcion", "Importe","Saldo"),show="headings",height=1)
        for col in ("Fecha","Descripcion","Importe","Saldo"):
            apertura_tree.heading(col,text=col)
            apertura_tree.column(col,anchor="center",width=170)
        fecha_apertura = datetime.now().strftime("%d/%m/%Y %H:%M")
        apertura_tree.insert("","end",values=(fecha_apertura,"APERTURA DE CAJA",f"${self.monto_apertura:.2f}",f"${self.monto_apertura:.2f}"))
        apertura_tree.pack(pady=10)

        stats_frame = ttk.Frame(frame_efectivo)
        stats_frame.pack(pady=10,fill="x")


        #Esto es temporal
        ventas = self.ventas_realizadas
        total_clientes = len(ventas)
        total_ventas = sum(v.total() for v in ventas)
        promedio_ventas = total_ventas / total_clientes if total_clientes else 0
        ventas_cta_cte = sum(v.total() for v in ventas if v.metodo_pago and v.metodo_pago.tipo == "Tarjeta")
        saldo_sistema = total_ventas
        importe_en_caja = self.monto_apertura
        diferencia = importe_en_caja - saldo_sistema

        izquierda = ttk.Frame(stats_frame)
        izquierda.pack(side="left",padx=20)

        ttk.Label(izquierda,text=f"Total Clientes: {total_clientes:.2f}").pack(anchor="w")
        ttk.Label(izquierda,text=f"Total Ventas: {total_ventas:.2f}").pack(anchor="w")
        ttk.Label(izquierda,text=f" Ventas Productos: {promedio_ventas:.2f}").pack(anchor="w")
        ttk.Label(izquierda,text=f" Ventas Cta Cte: {ventas_cta_cte:.2f}").pack(anchor="w")

        derecha = ttk.Frame(stats_frame)
        derecha.pack(side="right",padx=20)

        ttk.Label(derecha,text=f"Saldo Sistema: ${saldo_sistema:.2f}",foreground="green").pack(anchor="e")
        ttk.Label(derecha, text=f"Importe En Caja: ${importe_en_caja:.2f}", foreground="red").pack(anchor="e")
        ttk.Label(derecha, text=f"Diferencia De Caja: ${diferencia:.2f}").pack(anchor="e")

        botones = ttk.Frame(popup)
        botones.pack(pady=15,fill="x")

        ttk.Button(botones,text="Imprime").pack(side="left",padx=10)
        ttk.Button(botones,text="Aceptar",command=lambda:self.finalizar_caja(popup)).pack(side="right",padx=10)
        ttk.Button(botones,text="Cancelar",command=popup.destroy).pack(side="right",padx=10)


    def finalizar_caja(self,ventana):
        print("Caja cerrada correctamente")
        self.monto_apertura = None
        ventana.destroy()
        


    def accion_impresora(self):
        print("Impresora presionado")

    def accion_salir(self):
        print("Cerrando app...")
        self.destroy()

if __name__ == "__main__":
    app = CajaApp()
    app.mainloop()
