from cliente import Cliente
from database import obtener_conexion


def registrar_cliente(cliente):
    """
    Registra un cliente o administrador en la base de datos.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO cliente (
            nombre,
            rut,
            telefono,
            correo,
            contrasena_hash,
            rol
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        cliente.nombre,
        cliente.rut,
        cliente.telefono,
        cliente.correo,
        cliente.contrasena_hash,
        cliente.rol
    ))

    conexion.commit()
    id_cliente = cursor.lastrowid

    conexion.close()

    return id_cliente


def buscar_cliente_por_correo(correo):
    """
    Busca un usuario mediante su correo.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_cliente,
            nombre,
            rut,
            telefono,
            correo,
            contrasena_hash,
            rol
        FROM cliente
        WHERE correo = ?
    """, (correo,))

    cliente = cursor.fetchone()

    conexion.close()

    return cliente


def buscar_cliente_por_id(id_cliente):
    """
    Busca un usuario mediante su ID.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_cliente,
            nombre,
            rut,
            telefono,
            correo,
            contrasena_hash,
            rol
        FROM cliente
        WHERE id_cliente = ?
    """, (id_cliente,))

    cliente = cursor.fetchone()

    conexion.close()

    return cliente


def existe_cliente(correo, rut):
    """
    Comprueba si ya existe un usuario con ese correo o RUT.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_cliente
        FROM cliente
        WHERE correo = ? OR rut = ?
    """, (correo, rut))

    cliente = cursor.fetchone()

    conexion.close()

    return cliente is not None


def existe_administrador():
    """
    Comprueba si ya existe al menos un administrador.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_cliente
        FROM cliente
        WHERE rol = 'administrador'
        LIMIT 1
    """)

    administrador = cursor.fetchone()

    conexion.close()

    return administrador is not None