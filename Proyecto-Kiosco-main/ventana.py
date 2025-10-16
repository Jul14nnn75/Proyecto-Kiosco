import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from venta import Venta
from detalle_venta import DetalleVenta
from metodopago import MetodoPago

class POSWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Facturación")
        self.geometry("1000x650")
        self.configure(bg="#dfe6e9")

        self.venta = Venta("CONSUMIDOR FINAL")

        self.create_form()
        self.create_table()
        self.create_total_display()
        self.create_buttons()

        # Atajos de teclado
        self.bind_all("<KeyPress-F1>", lambda e: self.registrar_venta())
        self.bind_all("<KeyPress-F3>", lambda e: self.modificar_cantidad())
        self.bind_all("<KeyPress-F4>", lambda e: self.agregar_producto())
        self.bind_all("<KeyPress-F5>", lambda e: self.borrar_producto())
        self.bind_all("<KeyPress-F7>", lambda e: self.registrar_pago("Efectivo"))
        self.bind_all("<KeyPress-F8>", lambda e: self.registrar_pago("Tarjeta"))
        self.bind_all("<KeyPress-F9>", lambda e: self.agregar_varios())
        self.bind_all("<KeyPress-F12>", lambda e: self.cerrar_sistema())

    def create_form(self):
        frame = tk.LabelFrame(self, text="Datos de Factura", bg="#dfe6e9", padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=5)

        tk.Label(frame, text="Nombre:", bg="#dfe6e9", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="e", padx=5)
        tk.Label(frame, text="CONSUMIDOR FINAL", bg="#dfe6e9", font=("Arial", 10)).grid(row=0, column=1, sticky="w")

        tk.Label(frame, text="Fecha:", bg="#dfe6e9", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="e", padx=5)
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        tk.Label(frame, text=fecha_actual, bg="#dfe6e9", font=("Arial", 10)).grid(row=1, column=1, sticky="w")

        tk.Label(frame, text="Depósito:", bg="#dfe6e9", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="e", padx=5)
        tk.Label(frame, text="PRINCIPAL", bg="#dfe6e9", font=("Arial", 10)).grid(row=2, column=1, sticky="w")

        tk.Label(frame, text="Producto:", bg="#dfe6e9").grid(row=0, column=2)
        self.producto_entry = tk.Entry(frame, width=20)
        self.producto_entry.grid(row=0, column=3)
        self.producto_entry.focus_set()  # <-- Esto deja el cursor siempre en producto al abrir la ventana

        tk.Label(frame, text="Cantidad:", bg="#dfe6e9").grid(row=1, column=2)
        self.cantidad_entry = tk.Entry(frame, width=10)
        self.cantidad_entry.grid(row=1, column=3)
        self.cantidad_entry.insert(0, "1")

        tk.Label(frame, text="Precio:", bg="#dfe6e9").grid(row=2, column=2)
        self.precio_entry = tk.Entry(frame, width=10)
        self.precio_entry.grid(row=2, column=3)
        self.precio_entry.insert(0, "0.00")

        # Binding para que Enter agregue automáticamente el producto
        self.producto_entry.bind("<Return>", lambda e: self.agregar_producto())


    def create_table(self):
        table_frame = tk.Frame(self, bg="#dfe6e9")
        table_frame.pack(padx=10, pady=10)

        columns = ("Código", "Descripción", "Cantidad", "Venta", "Total")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180, anchor="center")
        self.tree.pack()

    def create_total_display(self):
        frame = tk.Frame(self, bg="#dfe6e9")
        frame.pack(pady=10)
        tk.Label(frame, text="TOTAL:", font=("Arial", 16, "bold"), bg="#dfe6e9").pack(side="left")
        self.total_label = tk.Label(frame, text="0.00", font=("Arial", 28, "bold"), fg="red", bg="#dfe6e9")
        self.total_label.pack(side="left", padx=20)

    def create_buttons(self):
        frame = tk.Frame(self, bg="#dfe6e9")
        frame.pack(pady=10)

        botones = [
            ("F1) Registrar", self.registrar_venta),
            ("F3) Cantidad", self.modificar_cantidad),
            ("F4) Agregar", self.agregar_producto),
            ("F5) Borrar", self.borrar_producto),
            ("F7) Efectivo", lambda: self.registrar_pago("Efectivo")),
            ("F8) Tarjeta", lambda: self.registrar_pago("Tarjeta")),
            ("F9) Varios", self.agregar_varios),
            ("F12) Cerrar", self.cerrar_sistema)
        ]

        for i, (text, cmd) in enumerate(botones):
            tk.Button(frame, text=text, width=12, height=2, font=("Arial", 9), command=cmd).grid(row=0, column=i, padx=5)

    def agregar_producto(self):
        producto = self.producto_entry.get().strip()
        if not producto:
            messagebox.showwarning("Error", "Debe ingresar un nombre de producto.")
            return

        try:
            cantidad = int(self.cantidad_entry.get())
            precio = float(self.precio_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Cantidad y precio deben ser numéricos.")
            return

        detalle = DetalleVenta(producto, cantidad, precio)
        self.venta.agregar_detalle(detalle)

        self.tree.insert("", "end", values=(producto, producto, cantidad, f"${precio:.2f}", f"${detalle.subtotal():.2f}"))
        self.actualizar_total()

        self.producto_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)
        self.precio_entry.insert(0, "0.00")
        self.cantidad_entry.delete(0, tk.END)
        self.cantidad_entry.insert(0, "1")

    def borrar_producto(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            index = self.tree.index(item)
            self.tree.delete(item)
            del self.venta.detalles[index]
        elif self.tree.get_children():
            item = self.tree.get_children()[-1]
            index = self.tree.index(item)
            self.tree.delete(item)
            del self.venta.detalles[index]
        else:
            messagebox.showinfo("Aviso", "No hay productos para borrar.")
            return

        self.actualizar_total()

    def modificar_cantidad(self):
        try:
            nueva_cantidad = simpledialog.askinteger("Cantidad", "Ingrese la cantidad para esta venta:", minvalue=1)
            if nueva_cantidad:
                self.cantidad_entry.delete(0, tk.END)
                self.cantidad_entry.insert(0, str(nueva_cantidad))
                self.agregar_producto()
        except:
            messagebox.showerror("Error", "Cantidad inválida.")

    def actualizar_total(self):
        total = self.venta.total()
        self.total_label.config(text=f"{total:.2f}")

    def registrar_pago(self, tipo):
        if not self.venta.detalles:
            messagebox.showwarning("Advertencia", "No hay productos para registrar.")
            return

        total_comprobante = self.venta.total()

        # Ventana de cierre de comprobante
        ventana = tk.Toplevel(self)
        ventana.title(f"Cierre de Comprobante - {tipo}")
        ventana.geometry("350x300")
        ventana.configure(bg="#dfe6e9")

        tk.Label(ventana, text=f"Total Comprobante: {total_comprobante:.2f}",
                 font=("Arial", 12, "bold"), bg="#dfe6e9").pack(pady=5)

        tk.Label(ventana, text="Importe Efectivo:", bg="#dfe6e9").pack()
        entry_efectivo = tk.Entry(ventana)
        entry_efectivo.pack()
        entry_efectivo.insert(0, f"{total_comprobante:.2f}")

        tk.Label(ventana, text="Importe Recibido:", bg="#dfe6e9").pack()
        entry_recibido = tk.Entry(ventana)
        entry_recibido.pack()
        entry_recibido.insert(0, f"{total_comprobante:.2f}")

        tk.Label(ventana, text="Importe Vuelto:", bg="#dfe6e9").pack()
        entry_vuelto = tk.Entry(ventana)
        entry_vuelto.pack()
        entry_vuelto.insert(0, "0.00")
        entry_vuelto.config(state="readonly")

        tk.Label(ventana, text="Total Cobrado:", bg="#dfe6e9").pack()
        entry_cobrado = tk.Entry(ventana)
        entry_cobrado.pack()
        entry_cobrado.insert(0, f"{total_comprobante:.2f}")
        entry_cobrado.config(state="readonly")

        # Función para calcular vuelto dinámicamente
        def calcular_vuelto(event=None):
            try:
                recibido_val = float(entry_recibido.get())
                efectivo_val = float(entry_efectivo.get())
                entry_vuelto.config(state="normal")
                entry_vuelto.delete(0, tk.END)
                entry_vuelto.insert(0, f"{recibido_val - efectivo_val:.2f}")
                entry_vuelto.config(state="readonly")
            except:
                pass

        entry_efectivo.bind("<KeyRelease>", calcular_vuelto)
        entry_recibido.bind("<KeyRelease>", calcular_vuelto)

        # Función para confirmar venta
        def confirmar():
            try:
                calcular_vuelto()
                messagebox.showinfo("Éxito", "Venta registrada correctamente")
                ventana.destroy()

                # Limpiar tabla principal y reiniciar venta
                for item in self.tree.get_children():
                    self.tree.delete(item)
                self.venta = Venta("CONSUMIDOR FINAL")
                self.actualizar_total()
            except Exception as e:
                messagebox.showerror("Error", f"Hubo un problema: {e}")

        # Botones OK y Cancelar
        frame_botones = tk.Frame(ventana, bg="#dfe6e9")
        frame_botones.pack(pady=20)
        tk.Button(frame_botones, text="OK", width=10, command=confirmar).grid(row=0, column=0, padx=10)
        tk.Button(frame_botones, text="Cancelar", width=10, command=ventana.destroy).grid(row=0, column=1, padx=10)

    def agregar_varios(self):
        precio = simpledialog.askfloat("VARIOS", "Ingrese el precio para producto VARIOS:")
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

        for item in self.tree.get_children():
            self.tree.delete(item)
        self.venta = Venta("CONSUMIDOR FINAL")
        self.actualizar_total()

    def cerrar_sistema(self):
        confirmar = messagebox.askyesno("Cerrar sistema", "¿Desea cerrar el sistema?")
        if confirmar:
            self.destroy()

if __name__ == "__main__":
    app = POSWindow()
    app.mainloop()
