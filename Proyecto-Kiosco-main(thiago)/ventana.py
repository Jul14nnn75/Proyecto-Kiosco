import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv, os
from venta import Venta
from detalle_venta import DetalleVenta
from metodopago import MetodoPago
from inventario import buscar_producto_por_codigo

class POSWindow(tk.Toplevel):
    def __init__(self, master=None, caja=None):
        super().__init__(master)
        self.title("Punto de Venta - Kiosco")
        self.geometry("800x450")
        self.configure(bg="#f0f0f0")

        # 🔥 POSICIÓN: Arriba y centrado
        self.posicionar_arriba_centrado()

        self.caja = caja
        self.venta = Venta("CONSUMIDOR FINAL")
        self._ventana_cantidad = None

        self.crear_interfaz()

    def posicionar_arriba_centrado(self):
        self.update_idletasks()
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()
        ancho_ventana = 800
        alto_ventana = 450
        x = (ancho_pantalla - ancho_ventana) // 2
        y = 50
        self.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    def crear_interfaz(self):
        # Título principal
        titulo_frame = tk.Frame(self, bg="#2c3e50", height=60)
        titulo_frame.pack(fill="x", padx=10, pady=10)
        titulo_frame.pack_propagate(False)
        
        tk.Label(titulo_frame, text="Punto de Venta - Kiosco", 
                font=("Arial", 18, "bold"), 
                bg="#2c3e50", fg="white").pack(expand=True)

        # Frame principal con dos columnas
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Columna izquierda - Formulario
        left_frame = tk.Frame(main_frame, bg="#f0f0f0")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Frame Registrar Venta
        form_frame = tk.LabelFrame(left_frame, text="Registrar Venta", 
                                  bg="#ffffff", fg="#2c3e50",
                                  font=("Arial", 11, "bold"),
                                  padx=10, pady=10)
        form_frame.pack(fill="x", pady=(0, 10))

        # Fila 1: Cliente y Código
        fila1 = tk.Frame(form_frame, bg="#ffffff")
        fila1.pack(fill="x", pady=5)

        tk.Label(fila1, text="Cliente:", bg="#ffffff", 
                font=("Arial", 10, "bold")).pack(side="left", padx=(0, 5))
        self.cliente_var = tk.StringVar(value="CONSUMIDOR FINAL")
        tk.Entry(fila1, textvariable=self.cliente_var, width=20,
                font=("Arial", 10), relief="solid", bd=1).pack(side="left", padx=(0, 20))

        tk.Label(fila1, text="Código de producto:", bg="#ffffff",
                font=("Arial", 10, "bold")).pack(side="left", padx=(0, 5))
        self.codigo_entry = tk.Entry(fila1, width=15, font=("Arial", 10),
                                   relief="solid", bd=1)
        self.codigo_entry.pack(side="left")
        self.codigo_entry.focus_set()
        self.codigo_entry.bind("<Return>", self.buscar_y_agregar)

        # Fila 2: Fecha y Descripción
        fila2 = tk.Frame(form_frame, bg="#ffffff")
        fila2.pack(fill="x", pady=5)

        tk.Label(fila2, text="Fecha:", bg="#ffffff",
                font=("Arial", 10, "bold")).pack(side="left", padx=(0, 5))
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        tk.Label(fila2, text=fecha_actual, bg="#ffffff",
                font=("Arial", 10)).pack(side="left", padx=(0, 20))

        tk.Label(fila2, text="Descripción:", bg="#ffffff",
                font=("Arial", 10, "bold")).pack(side="left", padx=(0, 5))
        self.descripcion_var = tk.StringVar()
        tk.Label(fila2, textvariable=self.descripcion_var, bg="#ffffff",
                font=("Arial", 10), width=20, anchor="w").pack(side="left")

        # Fila 3: Cantidad y Precio
        fila3 = tk.Frame(form_frame, bg="#ffffff")
        fila3.pack(fill="x", pady=5)

        tk.Label(fila3, text="Cantidad actual:", bg="#ffffff",
                font=("Arial", 10, "bold")).pack(side="left", padx=(0, 5))
        self.cantidad_var = tk.IntVar(value=1)
        tk.Label(fila3, textvariable=self.cantidad_var, bg="#ffffff",
                font=("Arial", 10), width=5).pack(side="left", padx=(0, 20))

        tk.Label(fila3, text="Precio unitario:", bg="#ffffff",
                font=("Arial", 10, "bold")).pack(side="left", padx=(0, 5))
        self.precio_var = tk.StringVar(value="0.00")
        tk.Label(fila3, textvariable=self.precio_var, bg="#ffffff",
                font=("Arial", 10), width=10).pack(side="left")

        # Frame Detalle de Venta
        table_frame = tk.LabelFrame(left_frame, text="Detalle de Venta",
                                   bg="#ffffff", fg="#2c3e50",
                                   font=("Arial", 11, "bold"),
                                   padx=10, pady=10)
        table_frame.pack(fill="both", expand=True, pady=(0, 10))

        # Tabla
        columns = ("Código", "Descripción", "Cantidad", "Precio Unit.", "Subtotal")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        
        self.tree.column("Descripción", width=200)
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Columna derecha - Total y Botones
        right_frame = tk.Frame(main_frame, bg="#f0f0f0", width=200)
        right_frame.pack(side="right", fill="y", padx=(5, 0))
        right_frame.pack_propagate(False)

        # Display del Total
        total_frame = tk.LabelFrame(right_frame, text="Total", 
                                   bg="#ffffff", fg="#2c3e50",
                                   font=("Arial", 11, "bold"),
                                   padx=10, pady=10)
        total_frame.pack(fill="x", pady=(0, 10))

        self.total_label = tk.Label(total_frame, text="$ 0.00",
                                   font=("Arial", 24, "bold"),
                                   fg="#e74c3c", bg="#ffffff")
        self.total_label.pack()

        # Botones en columna
        botones = [
            ("Registrar Venta (F7)", self.registrar_venta, "#27ae60"),
            ("Eliminar Producto (F5)", self.borrar_producto, "#e74c3c"),
            ("Modificar Cantidad (F3)", self.modificar_cantidad, "#3498db"),
            ("Producto Varios (F9)", self.agregar_varios, "#34495e"),
            ("Ver Historial", self.ver_historial, "#1abc9c"),
            ("Cerrar (F12)", self.cerrar_sistema, "#95a5a6")
        ]

        for texto, cmd, color in botones:
            btn = tk.Button(right_frame, text=texto, command=cmd,
                          font=("Arial", 9, "bold"), bg=color, fg="white",
                          width=18, height=2, relief="solid", bd=1)
            btn.pack(fill="x", pady=3)

        self.crear_shortcuts()

    def crear_shortcuts(self):
        self.bind("<F3>", lambda e: self.modificar_cantidad())
        self.bind("<F5>", lambda e: self.borrar_producto())
        self.bind("<F7>", lambda e: self.registrar_venta())
        self.bind("<F9>", lambda e: self.agregar_varios())
        self.bind("<F12>", lambda e: self.cerrar_sistema())

    # ... (los métodos restantes se mantienen igual que en la versión anterior)
    def buscar_y_agregar(self, event=None):
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
        if self._ventana_cantidad and self._ventana_cantidad.winfo_exists():
            self._ventana_cantidad.lift()
            return

        self._ventana_cantidad = tk.Toplevel(self)
        self._ventana_cantidad.title("Cambiar cantidad")
        self._ventana_cantidad.geometry("250x140")
        self._ventana_cantidad.configure(bg="#f8f8f8")
        self._ventana_cantidad.transient(self)
        self._ventana_cantidad.grab_set()

        tk.Label(self._ventana_cantidad, text="Nueva cantidad:",
                 bg="#f8f8f8", font=("Arial", 11)).pack(pady=10)
        entry = tk.Entry(self._ventana_cantidad, font=("Arial", 12),
                         justify="center")
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
        ventana = tk.Toplevel(self)
        ventana.title("Producto VARIOS")
        ventana.geometry("280x150")
        ventana.configure(bg="#f8f8f8")
        ventana.transient(self)
        ventana.grab_set()

        tk.Label(ventana, text="Ingrese precio:", bg="#f8f8f8",
                 font=("Arial", 11)).pack(pady=10)
        entry = tk.Entry(ventana, font=("Arial", 12), justify="center")
        entry.pack(pady=5)
        entry.focus()

        def confirmar():
            try:
                precio = float(entry.get().replace(",", "."))
                detalle = DetalleVenta("VARIOS", 1, precio)
                self.venta.agregar_detalle(detalle)
                self.tree.insert("", "end", values=(
                    "VARIOS", "VARIOS", 1, f"${precio:.2f}", f"${precio:.2f}"))
                self.actualizar_total()
            except:
                pass
            ventana.destroy()

        entry.bind("<Return>", lambda e: confirmar())
        entry.bind("<Escape>", lambda e: ventana.destroy())

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

    def registrar_venta(self, event=None):
        if not self.venta.detalles:
            messagebox.showerror("Error", "No hay productos en la venta.")
            return

        total = self.venta.total()

        popup = tk.Toplevel(self)
        popup.title("Cierre de Comprobante - Efectivo")
        popup.configure(bg="#eaf2f8")
        popup.transient(self)
        popup.grab_set()
        popup.lift()
        popup.attributes("-topmost", True)

        ancho, alto = 400, 380
        self.update_idletasks()
        x_principal = self.winfo_x()
        y_principal = self.winfo_y()
        w_principal = self.winfo_width()
        h_principal = self.winfo_height()
        x = x_principal + (w_principal // 2) - (ancho // 2)
        y = y_principal + (h_principal // 2) - (alto // 2)
        popup.geometry(f"{ancho}x{alto}+{x}+{y}")

        tk.Label(popup, text=f"Total Comprobante: ${total:.2f}",
                 font=("Arial", 16, "bold"),
                 fg="white", bg="#e74c3c",
                 padx=10, pady=10).pack(fill="x", pady=(10, 20))

        frame = tk.Frame(popup, bg="#eaf2f8")
        frame.pack(pady=5)

        def crear_fila(texto, var):
            tk.Label(frame, text=texto, font=("Arial", 12, "bold"),
                     bg="#eaf2f8", fg="#2c3e50").pack(anchor="w", pady=5)
            e = tk.Entry(frame, textvariable=var, font=("Arial", 12),
                         justify="center", relief="solid", bd=1, width=20)
            e.pack(pady=3)
            return e

        var_efectivo = tk.StringVar(value=f"{total:.2f}")
        var_recibido = tk.StringVar(value=f"{total:.2f}")
        var_vuelto = tk.StringVar(value="0.00")

        entry_efectivo = crear_fila("Importe Efectivo:", var_efectivo)
        entry_recibido = crear_fila("Importe Recibido:", var_recibido)
        entry_vuelto = crear_fila("Importe Vuelto:", var_vuelto)

        entry_recibido.focus()

        def calcular_vuelto(*_):
            try:
                recibido = float(var_recibido.get().replace(",", "."))
                total_efectivo = float(var_efectivo.get().replace(",", "."))
                vuelto = recibido - total_efectivo
                var_vuelto.set(f"{vuelto:.2f}")
            except:
                var_vuelto.set("0.00")

        def confirmar_pago(*_):
            try:
                detalles_str = "; ".join(
                    [f"{d.producto} x{d.cantidad} (${d.precio_unitario:.2f})"
                     for d in self.venta.detalles]
                )
                self._guardar_venta_csv_writer(total, detalles_str)
                if self.caja:
                    try:
                        self.caja._registrar_venta_en_caja(total, detalles_str)
                    except Exception:
                        pass
                self.limpiar_venta()
                popup.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        def cancelar(*_):
            popup.destroy()

        btn_frame = tk.Frame(popup, bg="#eaf2f8")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Confirmar Pago", command=confirmar_pago,
                  bg="#27ae60", fg="white", font=("Arial", 12, "bold"),
                  padx=20, pady=10, width=14).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancelar", command=cancelar,
                  bg="#c0392b", fg="white", font=("Arial", 12, "bold"),
                  padx=20, pady=10, width=14).pack(side="left", padx=10)

        entry_recibido.bind("<KeyRelease>", calcular_vuelto)
        popup.bind("<Return>", confirmar_pago)
        popup.bind("<Escape>", cancelar)

    def _guardar_venta_csv_writer(self, total, detalles_str):
        os.makedirs("data/ventas", exist_ok=True)
        ruta = os.path.join("data/ventas", "ventas.csv")
        existe = os.path.isfile(ruta)
        with open(ruta, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not existe:
                writer.writerow(["Fecha", "Cliente", "Total", "Detalles"])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                self.venta.cliente,
                f"{total:.2f}",
                detalles_str
            ])

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
            return
        historial = ""
        with open(ruta, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                historial += f"Fecha: {row[0]}, Cliente: {row[1]}, Total: ${row[2]}, Detalles: {row[3]}\n"
        top = tk.Toplevel(self)
        top.title("Historial de Ventas")
        top.geometry("800x400")
        text = tk.Text(top, wrap="word", font=("Arial", 10))
        text.pack(fill="both", expand=True)
        text.insert("1.0", historial)
        text.configure(state="disabled")