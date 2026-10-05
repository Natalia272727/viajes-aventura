from database import obtener_conexion


def registrar_destino(nombre, ubicacion, costo_base):
    """
    Registra un nuevo destino disponible.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO destino (
            nombre,
            ubicacion,
            costo_base,
            disponible
        )
        VALUES (?, ?, ?, 1)
    """, (
        nombre,
        ubicacion,
        costo_base
    ))

    conexion.commit()
    id_destino = cursor.lastrowid

    conexion.close()

    return id_destino


def modificar_destino(
    id_destino,
    nombre,
    ubicacion,
    costo_base
):
    """
    Modifica la información de un destino.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE destino
        SET nombre = ?,
            ubicacion = ?,
            costo_base = ?
        WHERE id_destino = ?
    """, (
        nombre,
        ubicacion,
        costo_base,
        id_destino
    ))

    conexion.commit()

    modificado = cursor.rowcount > 0

    conexion.close()

    return modificado


def marcar_destino_no_disponible(id_destino):
    """
    Marca un destino como no disponible.
    No lo elimina físicamente de la base de datos.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE destino
        SET disponible = 0
        WHERE id_destino = ?
    """, (id_destino,))

    conexion.commit()

    modificado = cursor.rowcount > 0

    conexion.close()

    return modificado


def listar_destinos_disponibles():
    """
    Obtiene todos los destinos actualmente disponibles.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_destino,
            nombre,
            ubicacion,
            costo_base
        FROM destino
        WHERE disponible = 1
        ORDER BY id_destino
    """)

    destinos = cursor.fetchall()

    conexion.close()

    return destinos


def obtener_destino_por_id(id_destino):
    """
    Obtiene un destino por su identificador.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_destino,
            nombre,
            ubicacion,
            costo_base,
            disponible
        FROM destino
        WHERE id_destino = ?
    """, (id_destino,))

    destino = cursor.fetchone()

    conexion.close()

    return destino