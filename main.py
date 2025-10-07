import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from venta import Venta
from detalle_venta import DetalleVenta
from metodopago import MetodoPago

class AppVenta:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Ventas - Kiosco")
        self.root.geometry("600x650")

        self.venta = None

        # --- Detalles ---
        frame_detalle = tk.LabelFrame(root, text="Agregar producto", padx=10, pady=10)
        frame_detalle.pack(pady=10, fill="x")

        tk.Label(frame_detalle, text="Producto:").grid(row=0, column=0)
        self.entry_producto = tk.Entry(frame_detalle)
        self.entry_producto.grid(row=0, column=1)

        tk.Label(frame_detalle, text="Cantidad:").grid(row=1, column=0)
        self.entry_cantidad = tk.Entry(frame_detalle)
        self.entry_cantidad.grid(row=1, column=1)

        tk.Label(frame_detalle, text="Precio:").grid(row=2, column=0)
        self.entry_precio = tk.Entry(frame_detalle)
        self.entry_precio.grid(row=2, column=1)

        tk.Button(frame_detalle, text="Agregar Producto [F7]", command=self.agregar_detalle).grid(row=3, column=0, columnspan=2, pady=5)

        # --- Tabla ---
        self.tree = ttk.Treeview(root, columns=("producto", "cantidad", "precio", "subtotal"), show="headings", height=10)
        for col in ("producto", "cantidad", "precio", "subtotal"):
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="center", width=120)
        self.tree.pack(pady=10)

        # --- Total ---
        self.label_total = tk.Label(root, text="Total: $0.00", font=("Arial", 12, "bold"))
        self.label_total.pack(pady=5)

        # --- Atajos visualizados ---
        self.label_atajos = tk.Label(root, text="Agregar[F7]  Eliminar[F5]  Cantidad[F3]  Varios[F9]", font=("Arial", 10, "bold"))
        self.label_atajos.pack(pady=5)

        # --- Botones de acción ---
        frame_botones = tk.Frame(root)
        frame_botones.pack(pady=5)

        tk.Button(frame_botones, text="Agregar [F7]", width=12, command=self.agregar_detalle).grid(row=0, column=0, padx=5)
        tk.Button(frame_botones, text="Eliminar [F5]", width=12, command=self.eliminar_producto).grid(row=0, column=1, padx=5)
        tk.Button(frame_botones, text="Cantidad [F3]", width=12, command=self.modificar_cantidad).grid(row=0, column=2, padx=5)
        tk.Button(frame_botones, text="Varios [F9]", width=12, command=self.agregar_varios).grid(row=0, column=3, padx=5)

        # --- Eventos de teclado globales ---
        self.root.bind_all("<Key>", self.atajos)

        # --- Inicializar venta ---
        self.iniciar_venta()

    def iniciar_venta(self):
        self.venta = Venta("Consumidor Final")

    def agregar_detalle(self):
        producto = self.entry_producto.get().strip()
        if not producto:
            messagebox.showwarning("Advertencia", "Ingrese nombre del producto o use F9 para 'Varios'")
            return

        try:
            cantidad_text = self.entry_cantidad.get().strip()
            cantidad = int(cantidad_text) if cantidad_text else 1
            precio = float(self.entry_precio.get())
        except ValueError:
            messagebox.showerror("Error", "Verifique los valores ingresados")
            return

        detalle = DetalleVenta(producto, cantidad, precio)
        self.venta.agregar_detalle(detalle)

        self.tree.insert("", "end", values=(producto, cantidad, f"${precio:.2f}", f"${detalle.subtotal():.2f}"))
        self.label_total.config(text=f"Total: ${self.venta.total():.2f}")

        self.entry_producto.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)

    def agregar_varios(self, event=None):
        # Producto genérico "Varios"
        producto = "Varios"

        try:
            # Solo pedimos precio unitario
            precio = simpledialog.askfloat("Varios", "Ingrese precio unitario:", initialvalue=0.0, minvalue=0.0)
            if precio is None:
                return
        except:
            messagebox.showerror("Error", "Valor inválido")
            return

        # Cantidad por defecto como 1
        cantidad = 1

        detalle = DetalleVenta(producto, cantidad, precio)
        self.venta.agregar_detalle(detalle)
        self.tree.insert("", "end", values=(producto, cantidad, f"${precio:.2f}", f"${detalle.subtotal():.2f}"))
        self.label_total.config(text=f"Total: ${self.venta.total():.2f}")

    def eliminar_producto(self, event=None):
        self.tree.focus_set()
        selected = self.tree.selection()
        items = self.tree.get_children()

        if selected:
            item = selected[0]
            index = self.tree.index(item)
            self.venta.detalles.pop(index)
            self.tree.delete(item)
        elif items:
            item = items[-1]
            self.venta.detalles.pop(-1)
            self.tree.delete(item)
        else:
            return

        self.label_total.config(text=f"Total: ${self.venta.total():.2f}")

    def modificar_cantidad(self, event=None):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un producto para modificar la cantidad")
            return

        # Mostramos un cartelito indicando "Cantidad"
        messagebox.showinfo("Cantidad", "Ingrese la nueva cantidad")

        item = selected[0]
        index = self.tree.index(item)
        detalle = self.venta.detalles[index]

        nueva_cantidad = simpledialog.askinteger("Modificar Cantidad",
                                                 f"Ingrese nueva cantidad para {detalle.producto}:",
                                                 initialvalue=detalle.cantidad, minvalue=1)
        if nueva_cantidad:
            detalle.cantidad = nueva_cantidad
            subtotal = detalle.subtotal()
            self.tree.item(item, values=(detalle.producto, detalle.cantidad, f"${detalle.precio_unitario:.2f}", f"${subtotal:.2f}"))
            self.label_total.config(text=f"Total: ${self.venta.total():.2f}")

    def registrar_venta(self, event=None):
        if not self.venta.detalles:
            messagebox.showwarning("Advertencia", "No hay productos para registrar")
            return
        metodo = MetodoPago("Efectivo", self.venta.total())
        self.venta.registrar_pago(metodo)
        messagebox.showinfo("Venta Registrada", str(self.venta))

        # Limpiar tabla y total
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.label_total.config(text="Total: $0.00")
        self.iniciar_venta()

    # --- Función central de atajos ---
    def atajos(self, event):
        if event.keysym == "F3":
            self.modificar_cantidad()
        elif event.keysym == "F5":
            self.eliminar_producto()
        elif event.keysym == "F7":
            self.agregar_detalle()
        elif event.keysym == "F9":
            self.agregar_varios()


if __name__ == "__main__":
    root = tk.Tk()
    app = AppVenta(root)
    root.mainloop()

