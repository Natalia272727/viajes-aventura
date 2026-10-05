from database import obtener_conexion


def registrar_reserva(reserva):
    """
    Registra una reserva en la base de datos.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO reserva (
            id_cliente,
            id_paquete,
            fecha_reserva,
            cantidad_personas,
            total
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        reserva.cliente,
        reserva.paquete,
        reserva.fecha_reserva,
        reserva.cantidad_personas,
        reserva.total
    ))

    conexion.commit()
    id_reserva = cursor.lastrowid

    conexion.close()

    return id_reserva


def listar_reservas_cliente(id_cliente):
    """
    Obtiene el historial de reservas de un cliente.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            r.id_reserva,
            r.id_cliente,
            p.nombre,
            p.fecha_salida,
            p.fecha_regreso,
            r.fecha_reserva,
            r.cantidad_personas,
            r.total
        FROM reserva r
        INNER JOIN paquete p
            ON r.id_paquete = p.id_paquete
        WHERE r.id_cliente = ?
        ORDER BY r.id_reserva DESC
    """, (id_cliente,))

    reservas = cursor.fetchall()

    conexion.close()

    return reservas


def obtener_cupos_disponibles(id_paquete):
    """
    Calcula los cupos disponibles de un paquete.

    Cupos disponibles =
    cupo máximo - personas reservadas.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            p.cupo_maximo,
            COALESCE(
                SUM(r.cantidad_personas),
                0
            )
        FROM paquete p
        LEFT JOIN reserva r
            ON p.id_paquete = r.id_paquete
        WHERE p.id_paquete = ?
        GROUP BY
            p.id_paquete,
            p.cupo_maximo
    """, (id_paquete,))

    resultado = cursor.fetchone()

    conexion.close()

    if resultado is None:
        return None

    cupo_maximo = resultado[0]
    personas_reservadas = resultado[1]

    return cupo_maximo - personas_reservadas


def contar_personas_reservadas(id_paquete):
    """
    Obtiene la cantidad total de personas
    que ya tienen reservas en un paquete.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT COALESCE(
            SUM(cantidad_personas),
            0
        )
        FROM reserva
        WHERE id_paquete = ?
    """, (id_paquete,))

    resultado = cursor.fetchone()

    conexion.close()

    return resultado[0]


def obtener_reserva_por_id(id_reserva):
    """
    Obtiene una reserva por su ID.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id_reserva,
            id_cliente,
            id_paquete,
            fecha_reserva,
            cantidad_personas,
            total
        FROM reserva
        WHERE id_reserva = ?
    """, (id_reserva,))

    reserva = cursor.fetchone()

    conexion.close()

    return reserva