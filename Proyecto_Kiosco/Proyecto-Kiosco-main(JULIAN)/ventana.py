import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from venta import Venta
from detalle_venta import DetalleVenta
from metodopago import MetodoPago
import os, csv, copy

class POSWindow(tk.Toplevel):
    def __init__(self, master=None, caja=None):
        super().__init__(master)
        self.title("Sistema de Facturación - Punto de Venta")
        self.geometry("1000x700")
        self.configure(bg="#dfe6e9")
        
        self.caja = caja
        self.venta = Venta("CONSUMIDOR FINAL")

        self.create_form()
        self.create_table()
        self.create_total_display()
        self.create_buttons()
        self.create_shortcuts()

    # ===============================
    # FORMULARIO PRINCIPAL
    # ===============================
    def create_form(self):
        frame = tk.LabelFrame(self, text="Datos de Factura", bg="#dfe6e9", padx=10, pady=10, font=("Arial", 10, "bold"))
        frame.pack(fill="x", padx=10, pady=5)

        tk.Label(frame, text="Cliente:", bg="#dfe6e9", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="e", padx=5)
        self.cliente_var = tk.StringVar(value="CONSUMIDOR FINAL")
        tk.Entry(frame, textvariable=self.cliente_var, width=20, font=("Arial", 10)).grid(row=0, column=1, sticky="w")

        tk.Label(frame, text="Fecha:", bg="#dfe6e9", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="e", padx=5)
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        tk.Label(frame, text=fecha_actual, bg="#dfe6e9", font=("Arial", 10)).grid(row=1, column=1, sticky="w")

        # Campos de producto
        tk.Label(frame, text="Producto:", bg="#dfe6e9", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=10)
        self.producto_entry = tk.Entry(frame, width=25, font=("Arial", 10))
        self.producto_entry.grid(row=0, column=3, padx=5)
        self.producto_entry.focus_set()

        tk.Label(frame, text="Cantidad:", bg="#dfe6e9", font=("Arial", 10, "bold")).grid(row=1, column=2, padx=10)
        self.cantidad_entry = tk.Entry(frame, width=10, font=("Arial", 10))
        self.cantidad_entry.grid(row=1, column=3, padx=5)
        self.cantidad_entry.insert(0, "1")

        tk.Label(frame, text="Precio:", bg="#dfe6e9", font=("Arial", 10, "bold")).grid(row=2, column=2, padx=10)
        self.precio_entry = tk.Entry(frame, width=10, font=("Arial", 10))
        self.precio_entry.grid(row=2, column=3, padx=5)
        self.precio_entry.insert(0, "0.00")

        tk.Button(frame, text="Agregar (Enter)", command=self.agregar_producto, 
                 bg="#27ae60", fg="white", font=("Arial", 9, "bold")).grid(row=0, column=4, rowspan=3, padx=10, sticky="ns")

        self.producto_entry.bind("<Return>", lambda e: self.agregar_producto())
        self.cantidad_entry.bind("<Return>", lambda e: self.agregar_producto())
        self.precio_entry.bind("<Return>", lambda e: self.agregar_producto())

    # ===============================
    # TABLA DE PRODUCTOS
    # ===============================
    def create_table(self):
        table_frame = tk.LabelFrame(self, text="Detalles de Venta", bg="#dfe6e9", padx=10, pady=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("Código", "Descripción", "Cantidad", "Precio Unit.", "Subtotal")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        
        widths = [150, 300, 100, 120, 120]
        for col, w in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # ===============================
    # TOTAL + DESCUENTO
    # ===============================
    def create_total_display(self):
        frame = tk.Frame(self, bg="#dfe6e9")
        frame.pack(fill="x", padx=10, pady=5)

        tk.Label(frame, text="TOTAL A PAGAR:", font=("Arial", 16, "bold"), bg="#dfe6e9", fg="#2c3e50").pack(side="left")
        self.total_label = tk.Label(frame, text="$ 0.00", font=("Arial", 28, "bold"), fg="#e74c3c", bg="#dfe6e9")
        self.total_label.pack(side="left", padx=20)

        tk.Label(frame, text="Descuento (%):", bg="#dfe6e9", font=("Arial", 12)).pack(side="left", padx=10)
        self.descuento_var = tk.DoubleVar(value=0.0)
        tk.Entry(frame, textvariable=self.descuento_var, width=5, font=("Arial", 12)).pack(side="left")

    # ===============================
    # BOTONES
    # ===============================
    def create_buttons(self):
        frame = tk.Frame(self, bg="#dfe6e9")
        frame.pack(fill="x", padx=10, pady=10)

        botones = [
            ("F1 - Registrar Venta", self.registrar_venta, "#27ae60"),
            ("F3 - Modificar Cantidad", self.modificar_cantidad, "#3498db"),
            ("F4 - Agregar Producto", self.agregar_producto, "#2980b9"),
            ("F5 - Eliminar Producto", self.borrar_producto, "#e74c3c"),
            ("F7 - Pago Efectivo", lambda: self.registrar_pago("Efectivo"), "#f39c12"),
            ("F8 - Pago Tarjeta", lambda: self.registrar_pago("Tarjeta"), "#9b59b6"),
            ("F9 - Producto Varios", self.agregar_varios, "#34495e"),
            ("Historial Ventas", self.ver_historial, "#1abc9c"),
            ("F12 - Cerrar", self.cerrar_sistema, "#95a5a6")
        ]

        for i, (text, cmd, color) in enumerate(botones):
            btn = tk.Button(frame, text=text, command=cmd, width=15, height=2,
                          font=("Arial", 9, "bold"), bg=color, fg="white",
                          relief="raised", bd=2)
            btn.grid(row=0, column=i, padx=3, pady=5)

    # ===============================
    # ATAJOS DE TECLADO
    # ===============================
    def create_shortcuts(self):
        self.bind("<F1>", lambda e: self.registrar_venta())
        self.bind("<F3>", lambda e: self.modificar_cantidad())
        self.bind("<F4>", lambda e: self.agregar_producto())
        self.bind("<F5>", lambda e: self.borrar_producto())
        self.bind("<F7>", lambda e: self.registrar_pago("Efectivo"))
        self.bind("<F8>", lambda e: self.registrar_pago("Tarjeta"))
        self.bind("<F9>", lambda e: self.agregar_varios())
        self.bind("<F12>", lambda e: self.cerrar_sistema())

    # ===============================
    # FUNCIONES DE PRODUCTOS
    # ===============================
    def agregar_producto(self):
        producto = self.producto_entry.get().strip()
        if not producto:
            messagebox.showwarning("Error", "Debe ingresar un nombre de producto.")
            self.producto_entry.focus_set()
            return

        try:
            cantidad = int(self.cantidad_entry.get())
            precio = float(self.precio_entry.get())
            if cantidad <= 0 or precio < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser mayor a 0 y precio debe ser un número válido.")
            return

        detalle = DetalleVenta(producto, cantidad, precio)
        self.venta.agregar_detalle(detalle)

        self.tree.insert("", "end", values=(
            f"PROD{len(self.venta.detalles):03d}", producto, cantidad, f"${precio:.2f}", f"${detalle.subtotal():.2f}"
        ))
        self.actualizar_total()

        self.producto_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)
        self.precio_entry.insert(0, "0.00")
        self.cantidad_entry.delete(0, tk.END)
        self.cantidad_entry.insert(0, "1")
        self.producto_entry.focus_set()

    def borrar_producto(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Aviso", "Seleccione un producto para eliminar.")
            return

        item = selected[0]
        valores = self.tree.item(item)["values"]
        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar producto: {valores[1]}?")
        
        if confirmar:
            index = self.tree.index(item)
            self.tree.delete(item)
            if index < len(self.venta.detalles):
                del self.venta.detalles[index]
            self.actualizar_total()

    def modificar_cantidad(self):
        try:
            nueva = simpledialog.askinteger("Modificar Cantidad", "Ingrese la nueva cantidad:", minvalue=1)
            if nueva:
                self.cantidad_entry.delete(0, tk.END)
                self.cantidad_entry.insert(0, str(nueva))
        except:
            messagebox.showerror("Error", "Cantidad inválida.")

    # ===============================
    # TOTAL + DESCUENTO
    # ===============================
    def actualizar_total(self):
        total = self.venta.total()
        desc = total * (self.descuento_var.get() / 100)
        total_final = total - desc
        self.total_label.config(text=f"$ {total_final:.2f}")

    # ===============================
    # PAGOS
    # ===============================
    def registrar_pago(self, tipo):
        if not self.venta.detalles:
            messagebox.showwarning("Advertencia", "No hay productos para registrar.")
            return

        total_comprobante = self.venta.total() * (1 - self.descuento_var.get()/100)

        ventana_pago = tk.Toplevel(self)
        ventana_pago.title(f"Cierre de Comprobante - {tipo}")
        ventana_pago.geometry("400x400")
        ventana_pago.configure(bg="#dfe6e9")
        ventana_pago.transient(self)
        ventana_pago.grab_set()

        tk.Label(ventana_pago, text=f"Total Comprobante: ${total_comprobante:.2f}",
                font=("Arial", 14, "bold"), bg="#dfe6e9", fg="#2c3e50").pack(pady=10)

        campos = [
            ("Importe Efectivo:", "entry_efectivo", f"{total_comprobante:.2f}"),
            ("Importe Recibido:", "entry_recibido", f"{total_comprobante:.2f}"),
            ("Importe Vuelto:", "entry_vuelto", "0.00")
        ]

        entries = {}
        for label, key, default in campos:
            tk.Label(ventana_pago, text=label, bg="#dfe6e9", font=("Arial", 10)).pack(pady=5)
            entry = tk.Entry(ventana_pago, font=("Arial", 10), justify="center")
            entry.pack(pady=2)
            entry.insert(0, default)
            if key == "entry_vuelto":
                entry.config(state="readonly")
            entries[key] = entry

        def calcular_vuelto(event=None):
            try:
                efectivo = float(entries["entry_efectivo"].get())
                recibido = float(entries["entry_recibido"].get())
                vuelto = recibido - efectivo
                entries["entry_vuelto"].config(state="normal")
                entries["entry_vuelto"].delete(0, tk.END)
                entries["entry_vuelto"].insert(0, f"{vuelto:.2f}")
                entries["entry_vuelto"].config(state="readonly")
            except:
                pass

        entries["entry_efectivo"].bind("<KeyRelease>", calcular_vuelto)
        entries["entry_recibido"].bind("<KeyRelease>", calcular_vuelto)

        def confirmar_pago(event=None):
            try:
                pago = MetodoPago(tipo, total_comprobante)
                self.venta.registrar_pago(pago)
                self.guardar_venta_csv(tipo)

                if self.caja and hasattr(self.caja, 'monto_apertura'):
                    self.caja.monto_apertura += total_comprobante

                ventana_pago.destroy()
                self.limpiar_venta()
            except Exception as e:
                messagebox.showerror("Error", f"Hubo un problema: {e}")

        frame_btn = tk.Frame(ventana_pago, bg="#dfe6e9")
        frame_btn.pack(pady=20)
        tk.Button(frame_btn, text="Confirmar Pago", command=confirmar_pago, bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                 width=12, height=2).pack(side="left", padx=10)
        tk.Button(frame_btn, text="Cancelar", command=ventana_pago.destroy, bg="#e74c3c", fg="white",
                 font=("Arial", 10, "bold"), width=12, height=2).pack(side="left", padx=10)
        entries["entry_recibido"].focus_set()

        ventana_pago.bind("<Return>", confirmar_pago)

    # ===============================
    # GUARDAR Y HISTORIAL
    # ===============================
    def guardar_venta_csv(self, tipo_pago):
        try:
            if not os.path.exists("data/ventas"):
                os.makedirs("data/ventas")
            ruta = os.path.join("data/ventas", "ventas.csv")
            existe = os.path.isfile(ruta)
            with open(ruta, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if not existe:
                    writer.writerow(["Fecha", "Cliente", "Total", "Método", "Detalles"])
                detalles_str = "; ".join([f"{d.producto} x{d.cantidad} (${d.precio_unitario:.2f})" for d in self.venta.detalles])
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    self.venta.cliente, f"{self.venta.total():.2f}", tipo_pago, detalles_str
                ])
        except Exception as err:
            print(f"Error al guardar venta: {err}")

    def ver_historial(self):
        ruta = os.path.join("data/ventas", "ventas.csv")
        if not os.path.isfile(ruta):
            messagebox.showinfo("Historial", "Aún no hay ventas registradas.")
            return

        win = tk.Toplevel(self)
        win.title("Historial de Ventas")
        win.geometry("700x400")
        win.configure(bg="#ecf0f1")
        win.transient(self)
        win.grab_set()

        cols = ["Fecha", "Cliente", "Total", "Método", "Detalles"]
        tree = ttk.Treeview(win, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, anchor="center", width=130)
        tree.pack(expand=True, fill="both", padx=10, pady=10)

        with open(ruta, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                tree.insert("", "end", values=row)

        tk.Button(win, text="Cerrar", command=win.destroy, bg="#e74c3c", fg="white", font=("Arial", 10, "bold")).pack(pady=5)

    # ===============================
    # VARIOS / LIMPIAR / SALIR
    # ===============================
    def limpiar_venta(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.venta = Venta(self.cliente_var.get())
        self.actualizar_total()
        self.producto_entry.focus_set()

    def agregar_varios(self):
        precio = simpledialog.askfloat("Producto VARIOS", "Ingrese el precio para producto VARIOS:", minvalue=0.0)
        if precio is None:
            return
        detalle = DetalleVenta("VARIOS", 1, precio)
        self.venta.agregar_detalle(detalle)
        self.tree.insert("", "end", values=("VARIOS", "VARIOS", 1, f"${precio:.2f}", f"${precio:.2f}"))
        self.actualizar_total()

    def registrar_venta(self):
        if not self.venta.detalles:
            messagebox.showwarning("Advertencia", "No hay productos para registrar.")
            return
        resumen = str(self.venta)
        messagebox.showinfo("Venta registrada", resumen)
        self.limpiar_venta()

    def cerrar_sistema(self):
        if messagebox.askyesno("Cerrar Sistema", "¿Está seguro que desea cerrar el punto de venta?"):
            self.destroy()
