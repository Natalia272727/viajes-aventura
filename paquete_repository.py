from database import obtener_conexion


def registrar_paquete(paquete):
    """
    Registra un nuevo paquete turístico.

    El precio queda almacenado en el momento
    de creación del paquete.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO paquete (
            nombre,
            fecha_salida,
            fecha_regreso,
            cupo_maximo,
            precio_persona
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        paquete.nombre,
        paquete.fecha_salida,
        paquete.fecha_regreso,
        paquete.cupo_maximo,
        paquete.precio_persona
    ))

    conexion.commit()

    id_paquete = cursor.lastrowid

    conexion.close()

    return id_paquete


def contar_personas_reservadas(id_paquete):
    """
    Obtiene la cantidad total de personas
    que ya tienen reservas en un paquete.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(cantidad_personas), 0)
        FROM reserva
        WHERE id_paquete = ?
    """, (id_paquete,))

    resultado = cursor.fetchone()

    conexion.close()

    return resultado[0]


def modificar_paquete(
    id_paquete,
    nombre,
    fecha_salida,
    fecha_regreso,
    cupo_maximo
):
    """
    Modifica los datos operativos de un paquete.

    El precio publicado NO se modifica.

    El nuevo cupo máximo no puede ser menor
    que la cantidad de personas ya reservadas.
    """

    personas_reservadas = contar_personas_reservadas(
        id_paquete
    )

    if cupo_maximo < personas_reservadas:
        raise ValueError(
            f"El nuevo cupo máximo no puede ser menor "
            f"que las {personas_reservadas} personas "
            f"ya reservadas."
        )

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE paquete
        SET nombre = ?,
            fecha_salida = ?,
            fecha_regreso = ?,
            cupo_maximo = ?
        WHERE id_paquete = ?
    """, (
        nombre,
        fecha_salida,
        fecha_regreso,
        cupo_maximo,
        id_paquete
    ))

    conexion.commit()

    modificado = cursor.rowcount > 0

    conexion.close()

    return modificado


def agregar_destino_a_paquete(
    id_paquete,
    id_destino
):
    """
    Relaciona un destino con un paquete.

    La clave primaria compuesta impide repetir
    el mismo destino dentro del mismo paquete.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            INSERT INTO paquete_destino (
                id_paquete,
                id_destino
            )
            VALUES (?, ?)
        """, (
            id_paquete,
            id_destino
        ))

        conexion.commit()

        resultado = True

    except Exception:
        conexion.rollback()
        resultado = False

    finally:
        conexion.close()

    return resultado


def quitar_destino_de_paquete(
    id_paquete,
    id_destino
):
    """
    Elimina la relación entre un paquete y un destino.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM paquete_destino
        WHERE id_paquete = ?
        AND id_destino = ?
    """, (
        id_paquete,
        id_destino
    ))

    conexion.commit()

    eliminado = cursor.rowcount > 0

    conexion.close()

    return eliminado


def obtener_paquete_por_id(id_paquete):
    """
    Obtiene un paquete mediante su ID.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_paquete,
            nombre,
            fecha_salida,
            fecha_regreso,
            cupo_maximo,
            precio_persona
        FROM paquete
        WHERE id_paquete = ?
    """, (id_paquete,))

    paquete = cursor.fetchone()

    conexion.close()

    return paquete


def listar_paquetes():
    """
    Obtiene todos los paquetes registrados.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_paquete,
            nombre,
            fecha_salida,
            fecha_regreso,
            cupo_maximo,
            precio_persona
        FROM paquete
        ORDER BY id_paquete
    """)

    paquetes = cursor.fetchall()

    conexion.close()

    return paquetes


def obtener_destinos_de_paquete(id_paquete):
    """
    Obtiene los destinos asociados a un paquete.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            d.id_destino,
            d.nombre,
            d.ubicacion,
            d.costo_base,
            d.disponible
        FROM destino d
        INNER JOIN paquete_destino pd
            ON d.id_destino = pd.id_destino
        WHERE pd.id_paquete = ?
        ORDER BY d.id_destino
    """, (id_paquete,))

    destinos = cursor.fetchall()

    conexion.close()

    return destinos


def contar_destinos_de_paquete(id_paquete):
    """
    Cuenta cuántos destinos tiene un paquete.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM paquete_destino
        WHERE id_paquete = ?
    """, (id_paquete,))

    resultado = cursor.fetchone()

    conexion.close()

    return resultado[0]