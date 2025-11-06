class MetodoPago:
    def __init__(self, tipo, monto):
        self.tipo = tipo  # Efectivo, Tarjeta, Transferencia
        self.monto = monto

    def __str__(self):
        return f"Pago con {self.tipo}: ${self.monto:.2f}"
