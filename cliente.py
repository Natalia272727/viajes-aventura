class Cliente:
    def __init__(
        self,
        nombre,
        rut,
        telefono,
        correo,
        contrasena_hash,
        rol="cliente"
    ):
        self.nombre = nombre
        self.rut = rut
        self.telefono = telefono
        self.correo = correo
        self.contrasena_hash = contrasena_hash
        self.rol = rol