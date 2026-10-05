class Reserva:
    def __init__(
        self,
        cliente,
        paquete,
        fecha_reserva,
        cantidad_personas,
        total
    ):
        self.cliente = cliente
        self.paquete = paquete
        self.fecha_reserva = fecha_reserva
        self.cantidad_personas = cantidad_personas
        self.total = total