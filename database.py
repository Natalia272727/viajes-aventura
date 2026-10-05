import sqlite3


NOMBRE_BASE_DATOS = "viajes_aventura.db"


def obtener_conexion():
    """
    Abre una conexión con la base de datos
    y activa las claves foráneas.
    """

    conexion = sqlite3.connect(NOMBRE_BASE_DATOS)

    conexion.execute("PRAGMA foreign_keys = ON")

    return conexion


def crear_base_datos():
    """
    Crea las tablas necesarias para el sistema
    si todavía no existen.

    También incorpora la columna rol en instalaciones
    anteriores que no la tuvieran.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # ======================================================
    # CLIENTES Y USUARIOS
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cliente (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            rut TEXT NOT NULL UNIQUE,
            telefono TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            contrasena_hash TEXT NOT NULL,
            rol TEXT NOT NULL DEFAULT 'cliente'
        )
    """)

    # Compatibilidad con una base creada anteriormente
    # sin la columna rol.
    cursor.execute("PRAGMA table_info(cliente)")
    columnas_cliente = [
        columna[1]
        for columna in cursor.fetchall()
    ]

    if "rol" not in columnas_cliente:
        cursor.execute("""
            ALTER TABLE cliente
            ADD COLUMN rol TEXT NOT NULL DEFAULT 'cliente'
        """)

    # ======================================================
    # DESTINOS
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS destino (
            id_destino INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            ubicacion TEXT NOT NULL,
            costo_base REAL NOT NULL,
            disponible INTEGER NOT NULL DEFAULT 1
        )
    """)

    # ======================================================
    # PAQUETES
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paquete (
            id_paquete INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            fecha_salida TEXT NOT NULL,
            fecha_regreso TEXT NOT NULL,
            cupo_maximo INTEGER NOT NULL,
            precio_persona REAL NOT NULL
        )
    """)

    # ======================================================
    # RELACIÓN PAQUETE - DESTINO
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paquete_destino (
            id_paquete INTEGER NOT NULL,
            id_destino INTEGER NOT NULL,

            PRIMARY KEY (id_paquete, id_destino),

            FOREIGN KEY (id_paquete)
                REFERENCES paquete(id_paquete)
                ON DELETE CASCADE,

            FOREIGN KEY (id_destino)
                REFERENCES destino(id_destino)
                ON DELETE RESTRICT
        )
    """)

    # ======================================================
    # RESERVAS
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reserva (
            id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            id_paquete INTEGER NOT NULL,
            fecha_reserva TEXT NOT NULL,
            cantidad_personas INTEGER NOT NULL,
            total REAL NOT NULL,

            FOREIGN KEY (id_cliente)
                REFERENCES cliente(id_cliente)
                ON DELETE RESTRICT,

            FOREIGN KEY (id_paquete)
                REFERENCES paquete(id_paquete)
                ON DELETE RESTRICT
        )
    """)

    # ======================================================
    # ÍNDICES
    # ======================================================

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_cliente_correo
        ON cliente(correo)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_cliente_rut
        ON cliente(rut)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_destino_disponible
        ON destino(disponible)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_paquete_destino_paquete
        ON paquete_destino(id_paquete)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_paquete_destino_destino
        ON paquete_destino(id_destino)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_reserva_cliente
        ON reserva(id_cliente)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_reserva_paquete
        ON reserva(id_paquete)
    """)

    conexion.commit()
    conexion.close()


if __name__ == "__main__":
    crear_base_datos()
    print("Base de datos creada correctamente.")