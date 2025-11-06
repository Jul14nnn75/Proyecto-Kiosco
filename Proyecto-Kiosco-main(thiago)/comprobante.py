import tkinter as tk
from tkinter import ttk, messagebox

class ComprobanteWindow(tk.Toplevel):
    def __init__(self, master, total, on_confirm):
        super().__init__(master)
        self.title("Cierre de Comprobante")
        self.geometry("400x320")
        self.configure(bg="#f4f4f4")
        self.resizable(False, False)
        self.total = total
        self.on_confirm = on_confirm  # callback a ventana principal

        # Traer la ventana al frente y hacerla activa
        self.transient(master)
        self.grab_set()
        self.focus_force()

        # Título y total
        tk.Label(self, text="Total Comprobante:", font=("Arial", 12, "bold"), bg="#f4f4f4").pack(pady=(15, 0))
        tk.Label(self, text=f"$ {self.total:.2f}", font=("Arial", 20, "bold"), fg="red", bg="#f4f4f4").pack(pady=(0, 10))

        # Método de pago
        metodo_frame = tk.Frame(self, bg="#f4f4f4")
        metodo_frame.pack(pady=5)
        self.metodo_pago = tk.StringVar(value="Efectivo")
        ttk.Radiobutton(metodo_frame, text="Efectivo", variable=self.metodo_pago, value="Efectivo").pack(side="left", padx=10)
        ttk.Radiobutton(metodo_frame, text="Tarjeta", variable=self.metodo_pago, value="Tarjeta").pack(side="left", padx=10)

        # Campos
        frame_campos = tk.Frame(self, bg="#f4f4f4")
        frame_campos.pack(pady=10)

        tk.Label(frame_campos, text="Importe Efectivo:", bg="#f4f4f4").grid(row=0, column=0, sticky="e", pady=5)
        self.efectivo_entry = tk.Entry(frame_campos, width=15, font=("Arial", 11), justify="center")
        self.efectivo_entry.grid(row=0, column=1)
        self.efectivo_entry.insert(0, f"{self.total:.2f}")

        tk.Label(frame_campos, text="Importe Recibido:", bg="#f4f4f4").grid(row=1, column=0, sticky="e", pady=5)
        self.recibido_entry = tk.Entry(frame_campos, width=15, font=("Arial", 11), justify="center")
        self.recibido_entry.grid(row=1, column=1)

        tk.Label(frame_campos, text="Importe Vuelto:", bg="#f4f4f4").grid(row=2, column=0, sticky="e", pady=5)
        self.vuelto_var = tk.StringVar(value="0.00")
        tk.Label(frame_campos, textvariable=self.vuelto_var, bg="#f4f4f4", font=("Arial", 11, "bold"), fg="green").grid(row=2, column=1)

        # Foco inicial en "Recibido"
        self.recibido_entry.focus_set()

        # Bind Enter para confirmar desde cualquier campo
        self.efectivo_entry.bind("<Return>", lambda e: self.confirmar())
        self.recibido_entry.bind("<Return>", lambda e: self.confirmar())
        self.bind("<Return>", lambda e: self.confirmar())
        self.bind("<Escape>", lambda e: self.destroy())

        # Actualiza vuelto al escribir
        self.recibido_entry.bind("<KeyRelease>", lambda e: self.actualizar_vuelto())

        # Botones
        botones = tk.Frame(self, bg="#f4f4f4")
        botones.pack(pady=20)
        tk.Button(botones, text="OK", width=10, bg="#2ecc71", fg="white", command=self.confirmar).pack(side="left", padx=10)
        tk.Button(botones, text="Cancelar", width=10, bg="#e74c3c", fg="white", command=self.destroy).pack(side="left", padx=10)

    def actualizar_vuelto(self):
        try:
            recibido_text = self.recibido_entry.get().strip()
            recibido = float(recibido_text) if recibido_text else self.total
            vuelto = recibido - self.total
            self.vuelto_var.set(f"{vuelto:.2f}" if vuelto >= 0 else "0.00")
        except ValueError:
            self.vuelto_var.set("0.00")

    def confirmar(self):
        try:
            metodo = self.metodo_pago.get()
            recibido_text = self.recibido_entry.get().strip()
            recibido = float(recibido_text) if recibido_text else self.total
            if recibido < self.total:
                messagebox.showwarning("Error", "El importe recibido es menor al total")
                return
            vuelto = recibido - self.total
            self.on_confirm(metodo, recibido, vuelto)
            self.destroy()
        except Exception as e:
            print("Error en comprobante:", e)
