import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from venta import Venta
from detalle_venta import DetalleVenta
from metodopago import MetodoPago
import copy

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

    def create_form(self):
        frame = tk.LabelFrame(self, text="Datos de Factura", bg="#dfe6e9", padx=10, pady=10, font=("Arial", 10, "bold"))
        frame.pack(fill="x", padx=10, pady=5)

        # Información del cliente
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

        # Botón rápido de agregar
        tk.Button(frame, text="Agregar (Enter)", command=self.agregar_producto, 
                 bg="#27ae60", fg="white", font=("Arial", 9, "bold")).grid(row=0, column=4, rowspan=3, padx=10, sticky="ns")

        # Bindings
        self.producto_entry.bind("<Return>", lambda e: self.agregar_producto())
        self.cantidad_entry.bind("<Return>", lambda e: self.agregar_producto())
        self.precio_entry.bind("<Return>", lambda e: self.agregar_producto())

    def create_table(self):
        table_frame = tk.LabelFrame(self, text="Detalles de Venta", bg="#dfe6e9", padx=10, pady=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("Código", "Descripción", "Cantidad", "Precio Unit.", "Subtotal")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        
        # Configurar columnas
        column_widths = [150, 300, 100, 120, 120]
        for col, width in zip(columns, column_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_total_display(self):
        frame = tk.Frame(self, bg="#dfe6e9")
        frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(frame, text="TOTAL A PAGAR:", font=("Arial", 16, "bold"), 
                bg="#dfe6e9", fg="#2c3e50").pack(side="left")
        
        self.total_label = tk.Label(frame, text="$ 0.00", font=("Arial", 28, "bold"), 
                                  fg="#e74c3c", bg="#dfe6e9")
        self.total_label.pack(side="left", padx=20)

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
            ("F12 - Cerrar", self.cerrar_sistema, "#95a5a6")
        ]

        for i, (text, cmd, color) in enumerate(botones):
            btn = tk.Button(frame, text=text, command=cmd, width=15, height=2,
                          font=("Arial", 9, "bold"), bg=color, fg="white",
                          relief="raised", bd=2)
            btn.grid(row=0, column=i, padx=3, pady=5)

    def create_shortcuts(self):
        self.bind("<F1>", lambda e: self.registrar_venta())
        self.bind("<F3>", lambda e: self.modificar_cantidad())
        self.bind("<F4>", lambda e: self.agregar_producto())
        self.bind("<F5>", lambda e: self.borrar_producto())
        self.bind("<F7>", lambda e: self.registrar_pago("Efectivo"))
        self.bind("<F8>", lambda e: self.registrar_pago("Tarjeta"))
        self.bind("<F9>", lambda e: self.agregar_varios())
        self.bind("<F12>", lambda e: self.cerrar_sistema())

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
            f"PROD{len(self.venta.detalles):03d}",
            producto, 
            cantidad, 
            f"${precio:.2f}", 
            f"${detalle.subtotal():.2f}"
        ))
        self.actualizar_total()

        # Limpiar campos y regresar foco
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
            nueva_cantidad = simpledialog.askinteger("Modificar Cantidad", 
                                                   "Ingrese la nueva cantidad:", 
                                                   minvalue=1, initialvalue=1)
            if nueva_cantidad:
                self.cantidad_entry.delete(0, tk.END)
                self.cantidad_entry.insert(0, str(nueva_cantidad))
        except:
            messagebox.showerror("Error", "Cantidad inválida.")

    def actualizar_total(self):
        total = self.venta.total()
        self.total_label.config(text=f"$ {total:.2f}")

    def registrar_pago(self, tipo):
        if not self.venta.detalles:
            messagebox.showwarning("Advertencia", "No hay productos para registrar.")
            return

        total_comprobante = self.venta.total()
        
        # Ventana de cierre de comprobante
        ventana_pago = tk.Toplevel(self)
        ventana_pago.title(f"Cierre de Comprobante - {tipo}")
        ventana_pago.geometry("400x400")
        ventana_pago.configure(bg="#dfe6e9")
        ventana_pago.transient(self)
        ventana_pago.grab_set()

        # Centrar ventana
        ventana_pago.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - ventana_pago.winfo_width()) // 2
        y = self.winfo_y() + (self.winfo_height() - ventana_pago.winfo_height()) // 2
        ventana_pago.geometry(f"+{x}+{y}")

        tk.Label(ventana_pago, text=f"Total Comprobante: ${total_comprobante:.2f}",
                font=("Arial", 14, "bold"), bg="#dfe6e9", fg="#2c3e50").pack(pady=10)

        # Campos de pago
        campos = [
            ("Importe Efectivo:", "entry_efectivo", f"{total_comprobante:.2f}"),
            ("Importe Recibido:", "entry_recibido", f"{total_comprobante:.2f}"),
            ("Importe Vuelto:", "entry_vuelto", "0.00"),
            ("Total Cobrado:", "entry_cobrado", f"{total_comprobante:.2f}")
        ]

        entries = {}
        for i, (label, key, default) in enumerate(campos):
            tk.Label(ventana_pago, text=label, bg="#dfe6e9", font=("Arial", 10)).pack(pady=5)
            entry = tk.Entry(ventana_pago, font=("Arial", 10), justify="center")
            entry.pack(pady=2)
            entry.insert(0, default)
            if key in ["entry_vuelto", "entry_cobrado"]:
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
                
                entries["entry_cobrado"].config(state="normal")
                entries["entry_cobrado"].delete(0, tk.END)
                entries["entry_cobrado"].insert(0, f"{efectivo:.2f}")
                entries["entry_cobrado"].config(state="readonly")
            except:
                pass

        entries["entry_efectivo"].bind("<KeyRelease>", calcular_vuelto)
        entries["entry_recibido"].bind("<KeyRelease>", calcular_vuelto)

        def confirmar_pago():
            try:
                # Registrar pago
                pago = MetodoPago(tipo, total_comprobante)
                self.venta.registrar_pago(pago)
                
                # Actualizar caja si existe
                if self.caja and hasattr(self.caja, 'monto_apertura') and self.caja.monto_apertura is not None:
                    self.caja.monto_apertura += total_comprobante
                    venta_copia = copy.deepcopy(self.venta)
                    self.caja.ventas_realizadas.append(venta_copia)
                    print(f"Caja actualizada: ${self.caja.monto_apertura:.2f}")

                messagebox.showinfo("Éxito", "Venta registrada correctamente")
                ventana_pago.destroy()
                self.limpiar_venta()
                
            except Exception as e:
                messagebox.showerror("Error", f"Hubo un problema: {e}")

        # Botones
        frame_botones = tk.Frame(ventana_pago, bg="#dfe6e9")
        frame_botones.pack(pady=20)
        
        tk.Button(frame_botones, text="Confirmar Pago", command=confirmar_pago,
                 bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                 width=12, height=2).pack(side="left", padx=10)
                 
        tk.Button(frame_botones, text="Cancelar", command=ventana_pago.destroy,
                 bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                 width=12, height=2).pack(side="left", padx=10)

        entries["entry_recibido"].focus_set()

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