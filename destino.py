class Destino:
    def __init__(
        self,
        nombre,
        ubicacion,
        costo_base,
        disponible=True
    ):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.costo_base = costo_base
        self.disponible = disponible