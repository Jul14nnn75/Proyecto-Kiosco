from datetime import datetime
from detalle_venta import DetalleVenta
from metodopago import MetodoPago

class Venta:
    def __init__(self, cliente):
        self.cliente = cliente
        self.fecha = datetime.now()
        self.detalles = []
        self.metodo_pago = None

    def agregar_detalle(self, detalle: DetalleVenta):
        self.detalles.append(detalle)

    def total(self):
        return sum(detalle.subtotal() for detalle in self.detalles)

    def registrar_pago(self, metodo_pago: MetodoPago):
        self.metodo_pago = metodo_pago

    def __str__(self):
        texto = f"🧾 Venta a {self.cliente} - {self.fecha.strftime('%d/%m/%Y %H:%M')}\n"
        for d in self.detalles:
            texto += f"  - {d}\n"
        texto += f"Total: ${self.total():.2f}\n"
        if self.metodo_pago:
            texto += f"{self.metodo_pago}\n"
        return texto
