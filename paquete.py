class Paquete:
    def __init__(
        self,
        nombre,
        fecha_salida,
        fecha_regreso,
        cupo_maximo,
        precio_persona
    ):
        self.nombre = nombre
        self.fecha_salida = fecha_salida
        self.fecha_regreso = fecha_regreso
        self.cupo_maximo = cupo_maximo
        self.precio_persona = precio_persona
        self.destinos = []