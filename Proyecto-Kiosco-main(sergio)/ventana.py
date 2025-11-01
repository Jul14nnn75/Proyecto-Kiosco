import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from datetime import datetime
from venta import Venta
from detalle_venta import DetalleVenta
from metodopago import MetodoPago
from inventario import buscar_producto_por_codigo
import os, csv
from comprobante import ComprobanteWindow


class POSWindow(tk.Toplevel):
    def __init__(self, master=None, caja=None):
        super().__init__(master)
        self.title("Punto de Venta - Kiosco")
        self.geometry("1100x700")
        self.configure(bg="#dfe6e9")

        self.caja = caja
        self.venta = Venta("CONSUMIDOR FINAL")
        self._ventana_cantidad = None  # Evita el warning por acceso antes de definir

        self.create_form()
        self.create_table()
        self.create_total_display()
        self.create_buttons()
        self.create_shortcuts()

    # ===============================
    # FORMULARIO PRINCIPAL
    # ===============================
    def create_form(self):
        frame = tk.LabelFrame(
            self, text="Registrar Venta", bg="#dfe6e9",
            padx=10, pady=10, font=("Arial", 10, "bold")
        )
        frame.pack(fill="x", padx=10, pady=10)

        # Cliente
        tk.Label(frame, text="Cliente:", bg="#dfe6e9", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="e", padx=5)
        self.cliente_var = tk.StringVar(value="CONSUMIDOR FINAL")
        tk.Entry(frame, textvariable=self.cliente_var, width=25, font=("Arial", 10)).grid(row=0, column=1, sticky="w")

        # Fecha
        tk.Label(frame, text="Fecha:", bg="#dfe6e9", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="e", padx=5)
        tk.Label(frame, text=datetime.now().strftime("%d/%m/%Y %H:%M"), bg="#dfe6e9", font=("Arial", 10)).grid(row=1, column=1, sticky="w")

        # Código de producto
        tk.Label(frame, text="Código de producto:", bg="#dfe6e9", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=10)
        self.codigo_entry = tk.Entry(frame, width=20, font=("Arial", 10))
        self.codigo_entry.grid(row=0, column=3, padx=5)
        self.codigo_entry.focus_set()
        self.codigo_entry.bind("<Return>", self.buscar_y_agregar)

        # Descripción automática
        tk.Label(frame, text="Descripción:", bg="#dfe6e9", font=("Arial", 10, "bold")).grid(row=1, column=2, padx=10)
        self.descripcion_var = tk.StringVar()
        tk.Label(frame, textvariable=self.descripcion_var, bg="#dfe6e9", font=("Arial", 10, "italic")).grid(row=1, column=3, sticky="w")

        # Cantidad actual (solo F3)
        tk.Label(frame, text="Cantidad actual:", bg="#dfe6e9", font=("Arial", 10, "bold")).grid(row=2, column=2, padx=10)
        self.cantidad_var = tk.IntVar(value=1)
        tk.Label(frame, textvariable=self.cantidad_var, bg="#dfe6e9", font=("Arial", 10, "italic")).grid(row=2, column=3, sticky="w")

        # Precio unitario
        tk.Label(frame, text="Precio unitario:", bg="#dfe6e9", font=("Arial", 10, "bold")).grid(row=3, column=2, padx=10)
        self.precio_var = tk.StringVar(value="0.00")
        tk.Label(frame, textvariable=self.precio_var, bg="#dfe6e9", font=("Arial", 10, "italic")).grid(row=3, column=3, sticky="w")

    # ===============================
    # TABLA
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
    # TOTAL
    # ===============================
    def create_total_display(self):
        frame = tk.Frame(self, bg="#dfe6e9")
        frame.pack(fill="x", padx=10, pady=10)
        self.total_label = tk.Label(
            frame, text="$ 0.00", font=("Arial", 36, "bold"),
            fg="#e74c3c", bg="#dfe6e9"
        )
        self.total_label.pack(side="right", padx=40)

    # ===============================
    # BOTONES Y ATAJOS
    # ===============================
    def create_buttons(self):
        frame = tk.Frame(self, bg="#dfe6e9")
        frame.pack(fill="x", padx=10, pady=10)

        botones = [
            ("Registrar Venta (F7)", self.registrar_venta, "#27ae60"),
            ("Eliminar Producto (F5)", self.borrar_producto, "#e74c3c"),
            ("Modificar Cantidad (F3)", self.modificar_cantidad, "#3498db"),
            ("Producto Varios (F9)", self.agregar_varios, "#34495e"),
            ("Ver Historial", self.ver_historial, "#1abc9c"),
            ("Cerrar (F12)", self.cerrar_sistema, "#95a5a6")
        ]

        for i, (text, cmd, color) in enumerate(botones):
            tk.Button(frame, text=text, command=cmd, width=20, height=2,
                     font=("Arial", 9, "bold"), bg=color, fg="white").grid(row=0, column=i, padx=3, pady=5)

    def create_shortcuts(self):
        self.bind("<F3>", lambda e: self.modificar_cantidad())
        self.bind("<F5>", lambda e: self.borrar_producto())
        self.bind("<F7>", lambda e: self.registrar_venta())
        self.bind("<F9>", lambda e: self.agregar_varios())
        self.bind("<F12>", lambda e: self.cerrar_sistema())

    # ===============================
    # FUNCIONES PRINCIPALES
    # ===============================
    def buscar_y_agregar(self, event=None):
        """Buscar el producto por código y agregarlo directamente."""
        codigo = self.codigo_entry.get().strip()
        if not codigo:
            return

        producto = buscar_producto_por_codigo(codigo)
        if not producto:
            self.bell()
            self.codigo_entry.delete(0, tk.END)
            self.codigo_entry.focus_set()
            return

        self.descripcion_var.set(producto["nombre"])
        self.precio_var.set(f"{producto['precio']:.2f}")
        self.agregar_producto(producto)

    def agregar_producto(self, producto):
        cantidad = self.cantidad_var.get()
        descripcion = producto["nombre"]
        precio = float(producto["precio"])

        detalle = DetalleVenta(descripcion, cantidad, precio)
        self.venta.agregar_detalle(detalle)
        self.tree.insert("", "end", values=(
            producto["codigo_articulo"], descripcion, cantidad,
            f"${precio:.2f}", f"${detalle.subtotal():.2f}"
        ))
        self.actualizar_total()

        self.codigo_entry.delete(0, tk.END)
        self.descripcion_var.set("")
        self.precio_var.set("0.00")
        self.cantidad_var.set(1)
        self.codigo_entry.focus_set()

    def modificar_cantidad(self, event=None):
        """Abrir una sola ventana para modificar cantidad."""
        if self._ventana_cantidad and self._ventana_cantidad.winfo_exists():
            self._ventana_cantidad.lift()
            self._ventana_cantidad.focus_force()
            return

        self._ventana_cantidad = tk.Toplevel(self)
        self._ventana_cantidad.title("Cantidad")
        self._ventana_cantidad.geometry("250x140")
        self._ventana_cantidad.resizable(False, False)
        self._ventana_cantidad.configure(bg="#f8f8f8")
        self._ventana_cantidad.transient(self)
        self._ventana_cantidad.grab_set()

        tk.Label(self._ventana_cantidad, text="Nueva cantidad:", bg="#f8f8f8", font=("Arial", 11)).pack(pady=10)
        entry = tk.Entry(self._ventana_cantidad, font=("Arial", 12), justify="center")
        entry.pack(pady=5)
        entry.focus()

        def confirmar():
            valor = entry.get().strip()
            if valor.isdigit() and int(valor) > 0:
                self.cantidad_var.set(int(valor))
            self._ventana_cantidad.destroy()

        entry.bind("<Return>", lambda e: confirmar())
        entry.bind("<Escape>", lambda e: self._ventana_cantidad.destroy())

    def agregar_varios(self):
        precio = simpledialog.askfloat("Producto VARIOS", "Ingrese el precio:", minvalue=0.0)
        if precio is None:
            return
        detalle = DetalleVenta("VARIOS", 1, precio)
        self.venta.agregar_detalle(detalle)
        self.tree.insert("", "end", values=("VARIOS", "VARIOS", 1, f"${precio:.2f}", f"${precio:.2f}"))
        self.actualizar_total()

    def borrar_producto(self):
        selected = self.tree.selection()
        if not selected:
            return
        item = selected[0]
        index = self.tree.index(item)
        self.tree.delete(item)
        if index < len(self.venta.detalles):
            del self.venta.detalles[index]
        self.actualizar_total()

    def actualizar_total(self):
        total = self.venta.total()
        self.total_label.config(text=f"$ {total:.2f}")

    # ===============================
    # REGISTRO / HISTORIAL
    # ===============================
    def registrar_venta(self):
        if not self.venta.detalles:
            return

        total = self.venta.total()
        # Abrir ventana de comprobante
        ComprobanteWindow(self, total, self.confirmar_pago)

    def confirmar_pago(self, metodo_pago, recibido, vuelto):
        # Guardar info en la venta
        self.venta.metodo_pago = metodo_pago
        self.venta.efectivo = recibido
        self.venta.recibido = recibido
        self.venta.vuelto = vuelto

        # Guardar la venta en CSV
        self.guardar_venta_csv()

        messagebox.showinfo("Venta Registrada", "La venta se ha registrado correctamente.")
        self.limpiar_venta()

    def guardar_venta_csv(self):
        try:
            if not os.path.exists("data/ventas"):
                os.makedirs("data/ventas")
            ruta = os.path.join("data/ventas", "ventas.csv")
            existe = os.path.isfile(ruta)
            with open(ruta, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if not existe:
                    writer.writerow(["Fecha", "Cliente", "Total", "Detalles"])
                detalles_str = "; ".join([f"{d.producto} x{d.cantidad} (${d.precio_unitario:.2f})" for d in self.venta.detalles])
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    self.venta.cliente,
                    f"{self.venta.total():.2f}",
                    detalles_str
                ])
        except Exception as err:
            print(f"Error al guardar venta: {err}")

    def limpiar_venta(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.venta = Venta(self.cliente_var.get())
        self.actualizar_total()
        self.codigo_entry.focus_set()

    def cerrar_sistema(self):
        self.destroy()

    def ver_historial(self):
        ruta = os.path.join("data/ventas", "ventas.csv")
        if not os.path.isfile(ruta):
            messagebox.showinfo("Historial de Ventas", "No hay ventas registradas aún.")
            return
        historial = ""
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    historial += f"Fecha: {row[0]}, Cliente: {row[1]}, Total: ${row[2]}, Detalles: {row[3]}\n"
            messagebox.showinfo("Historial de Ventas", historial)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el historial de ventas.\n{e}")
