from datetime import date

from database import crear_base_datos

from cliente_repository import (
    buscar_cliente_por_correo,
    existe_administrador
)

from destino_repository import (
    registrar_destino,
    modificar_destino,
    marcar_destino_no_disponible,
    listar_destinos_disponibles
)

from paquete_repository import (
    registrar_paquete,
    modificar_paquete,
    agregar_destino_a_paquete,
    quitar_destino_de_paquete,
    obtener_paquete_por_id,
    listar_paquetes,
    obtener_destinos_de_paquete
)

from reserva_repository import (
    registrar_reserva,
    listar_reservas_cliente,
    obtener_cupos_disponibles
)

from reserva import Reserva
from paquete import Paquete

from security import (
    autenticar_usuario,
    es_administrador,
    es_cliente,
    registrar_nuevo_cliente,
    crear_administrador
)

from validators import (
    validar_texto,
    validar_costo,
    validar_cupo,
    validar_fechas,
    validar_destinos_paquete,
    validar_cantidad_personas,
    validar_cupos_disponibles,
    validar_paquete_vigente
)


# ==========================================================
# FUNCIONES AUXILIARES
# ==========================================================

def leer_entero(mensaje):
    """
    Solicita un número entero al usuario.
    """
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Debe ingresar un número entero.")


def leer_decimal(mensaje):
    """
    Solicita un número decimal al usuario.
    """
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Debe ingresar un número válido.")


# ==========================================================
# REGISTRO
# ==========================================================

def menu_registro():

    print("\n=== REGISTRO DE CLIENTE ===")

    nombre = input("Nombre: ")
    rut = input("RUT: ")
    telefono = input("Teléfono: ")
    correo = input("Correo: ")
    contrasena = input("Contraseña: ")

    try:

        id_cliente = registrar_nuevo_cliente(
            nombre,
            rut,
            telefono,
            correo,
            contrasena
        )

        print("\nCliente registrado correctamente.")
        print(f"ID de cliente: {id_cliente}")

    except ValueError as error:
        print(f"\nNo fue posible registrar al cliente: {error}")

    except Exception as error:
        print(f"\nError inesperado: {error}")


# ==========================================================
# LOGIN
# ==========================================================

def iniciar_sesion():

    print("\n=== INICIO DE SESIÓN ===")

    correo = input("Correo: ")
    contrasena = input("Contraseña: ")

    usuario = autenticar_usuario(
        correo,
        contrasena
    )

    if usuario is None:
        print("\nCorreo o contraseña incorrectos.")
        return None

    print(f"\nBienvenido/a, {usuario[1]}.")
    print(f"Rol: {usuario[6]}")

    return usuario


# ==========================================================
# DESTINOS - ADMINISTRADOR
# ==========================================================

def administrar_destinos():

    while True:

        print("\n=== GESTIÓN DE DESTINOS ===")
        print("1. Registrar destino")
        print("2. Modificar destino")
        print("3. Marcar destino como no disponible")
        print("4. Listar destinos disponibles")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":

            print("\n--- Registrar destino ---")

            nombre = input("Nombre: ")
            ubicacion = input("Ubicación: ")
            costo_base = leer_decimal("Costo base: ")

            try:

                validar_texto(
                    nombre,
                    "Nombre del destino"
                )

                validar_texto(
                    ubicacion,
                    "Ubicación"
                )

                validar_costo(costo_base)

                id_destino = registrar_destino(
                    nombre,
                    ubicacion,
                    costo_base
                )

                print(
                    f"Destino registrado correctamente. "
                    f"ID: {id_destino}"
                )

            except ValueError as error:
                print(f"Error: {error}")

        elif opcion == "2":

            print("\n--- Modificar destino ---")

            id_destino = leer_entero(
                "ID del destino: "
            )

            nombre = input("Nuevo nombre: ")
            ubicacion = input("Nueva ubicación: ")
            costo_base = leer_decimal(
                "Nuevo costo base: "
            )

            try:

                validar_texto(
                    nombre,
                    "Nombre del destino"
                )

                validar_texto(
                    ubicacion,
                    "Ubicación"
                )

                validar_costo(costo_base)

                modificado = modificar_destino(
                    id_destino,
                    nombre,
                    ubicacion,
                    costo_base
                )

                if modificado:
                    print(
                        "Destino modificado correctamente."
                    )
                else:
                    print(
                        "No se encontró el destino."
                    )

            except ValueError as error:
                print(f"Error: {error}")

        elif opcion == "3":

            print("\n--- Deshabilitar destino ---")

            id_destino = leer_entero(
                "ID del destino: "
            )

            modificado = marcar_destino_no_disponible(
                id_destino
            )

            if modificado:
                print(
                    "Destino marcado como no disponible."
                )
            else:
                print(
                    "No se encontró el destino."
                )

        elif opcion == "4":

            print("\n--- DESTINOS DISPONIBLES ---")

            destinos = listar_destinos_disponibles()

            if not destinos:

                print(
                    "No existen destinos disponibles."
                )

            else:

                for destino in destinos:

                    print(
                        f"ID: {destino[0]} | "
                        f"{destino[1]} | "
                        f"{destino[2]} | "
                        f"Costo base: ${destino[3]:,.0f}"
                    )

        elif opcion == "0":
            break

        else:
            print("Opción no válida.")


# ==========================================================
# PAQUETES - ADMINISTRADOR
# ==========================================================

def calcular_precio_paquete(destinos):
    """
    Calcula el precio base del paquete a partir
    de los costos de sus destinos.

    Se aplica un margen del 20%.
    """

    costo_total = sum(
        destino[3]
        for destino in destinos
    )

    precio = costo_total * 1.20

    return round(precio, 2)


def crear_paquete_menu():

    print("\n=== CREAR PAQUETE ===")

    nombre = input(
        "Nombre del paquete: "
    )

    fecha_salida = input(
        "Fecha de salida (YYYY-MM-DD): "
    )

    fecha_regreso = input(
        "Fecha de regreso (YYYY-MM-DD): "
    )

    cupo_maximo = leer_entero(
        "Cupo máximo: "
    )

    try:

        validar_texto(
            nombre,
            "Nombre del paquete"
        )

        validar_fechas(
            fecha_salida,
            fecha_regreso
        )

        validar_cupo(
            cupo_maximo
        )

    except ValueError as error:

        print(f"Error: {error}")
        return

    destinos = listar_destinos_disponibles()

    if not destinos:

        print(
            "No existen destinos disponibles."
        )
        return

    print("\n=== DESTINOS DISPONIBLES ===")

    for destino in destinos:

        print(
            f"ID: {destino[0]} | "
            f"{destino[1]} | "
            f"{destino[2]} | "
            f"Costo: ${destino[3]:,.0f}"
        )

    print(
        "\nSeleccione entre 2 y 5 destinos."
    )

    ids_seleccionados = input(
        "IDs separados por coma: "
    )

    try:

        ids = [
            int(valor.strip())
            for valor in ids_seleccionados.split(",")
        ]

    except ValueError:

        print(
            "Los IDs deben ser números."
        )
        return

    if len(ids) != len(set(ids)):

        print(
            "No puede seleccionar destinos repetidos."
        )
        return

    destinos_seleccionados = [
        destino
        for destino in destinos
        if destino[0] in ids
    ]

    if len(destinos_seleccionados) != len(ids):

        print(
            "Uno o más destinos seleccionados "
            "no están disponibles."
        )
        return

    try:

        validar_destinos_paquete(
            destinos_seleccionados
        )

    except ValueError as error:

        print(f"Error: {error}")
        return

    precio_persona = calcular_precio_paquete(
        destinos_seleccionados
    )

    paquete = Paquete(
        nombre=nombre,
        fecha_salida=fecha_salida,
        fecha_regreso=fecha_regreso,
        cupo_maximo=cupo_maximo,
        precio_persona=precio_persona
    )

    id_paquete = registrar_paquete(
        paquete
    )

    for destino in destinos_seleccionados:

        agregar_destino_a_paquete(
            id_paquete,
            destino[0]
        )

    print(
        "\nPaquete creado correctamente."
    )

    print(
        f"ID: {id_paquete}"
    )

    print(
        f"Precio por persona: "
        f"${precio_persona:,.0f}"
    )


def consultar_paquetes():

    print("\n=== PAQUETES TURÍSTICOS ===")

    paquetes = listar_paquetes()

    if not paquetes:

        print(
            "No existen paquetes registrados."
        )
        return

    for paquete in paquetes:

        cupos = obtener_cupos_disponibles(
            paquete[0]
        )

        print(
            "\n-----------------------------"
        )

        print(
            f"ID: {paquete[0]}"
        )

        print(
            f"Nombre: {paquete[1]}"
        )

        print(
            f"Salida: {paquete[2]}"
        )

        print(
            f"Regreso: {paquete[3]}"
        )

        print(
            f"Cupo máximo: {paquete[4]}"
        )

        print(
            f"Cupos disponibles: {cupos}"
        )

        print(
            f"Precio por persona: "
            f"${paquete[5]:,.0f}"
        )

        destinos = obtener_destinos_de_paquete(
            paquete[0]
        )

        print("Destinos:")

        for destino in destinos:

            print(
                f"  - {destino[1]} "
                f"({destino[2]})"
            )


def administrar_paquetes():

    while True:

        print("\n=== GESTIÓN DE PAQUETES ===")
        print("1. Crear paquete")
        print("2. Consultar paquetes")
        print("3. Modificar paquete")
        print("0. Volver")

        opcion = input(
            "Seleccione una opción: "
        )

        if opcion == "1":

            crear_paquete_menu()

        elif opcion == "2":

            consultar_paquetes()

        elif opcion == "3":

            id_paquete = leer_entero(
                "ID del paquete: "
            )

            paquete = obtener_paquete_por_id(
                id_paquete
            )

            if paquete is None:

                print(
                    "No se encontró el paquete."
                )
                continue

            print(
                "\nNota: el precio publicado "
                "no será modificado."
            )

            nombre = input(
                "Nuevo nombre: "
            )

            fecha_salida = input(
                "Nueva fecha de salida "
                "(YYYY-MM-DD): "
            )

            fecha_regreso = input(
                "Nueva fecha de regreso "
                "(YYYY-MM-DD): "
            )

            cupo_maximo = leer_entero(
                "Nuevo cupo máximo: "
            )

            try:

                validar_texto(
                    nombre,
                    "Nombre del paquete"
                )

                validar_fechas(
                    fecha_salida,
                    fecha_regreso
                )

                validar_cupo(
                    cupo_maximo
                )

                modificado = modificar_paquete(
                    id_paquete,
                    nombre,
                    fecha_salida,
                    fecha_regreso,
                    cupo_maximo
                )

                if modificado:

                    print(
                        "Paquete modificado "
                        "correctamente."
                    )

                else:

                    print(
                        "No se pudo modificar "
                        "el paquete."
                    )

            except ValueError as error:

                print(
                    f"Error: {error}"
                )

        elif opcion == "0":

            break

        else:

            print(
                "Opción no válida."
            )


# ==========================================================
# RESERVAS - CLIENTE
# ==========================================================

def realizar_reserva(usuario):

    print("\n=== REALIZAR RESERVA ===")

    consultar_paquetes()

    id_paquete = leer_entero(
        "\nID del paquete que desea reservar: "
    )

    paquete = obtener_paquete_por_id(
        id_paquete
    )

    if paquete is None:

        print(
            "No se encontró el paquete."
        )
        return

    try:

        validar_paquete_vigente(
            paquete[2]
        )

    except ValueError as error:

        print(
            f"Error: {error}"
        )
        return

    cupos_disponibles = obtener_cupos_disponibles(
        id_paquete
    )

    print(
        f"Cupos disponibles: "
        f"{cupos_disponibles}"
    )

    cantidad_personas = leer_entero(
        "Cantidad de personas: "
    )

    try:

        validar_cantidad_personas(
            cantidad_personas
        )

        validar_cupos_disponibles(
            cantidad_personas,
            cupos_disponibles
        )

    except ValueError as error:

        print(
            f"Reserva rechazada: {error}"
        )
        return

    total = (
        cantidad_personas
        * paquete[5]
    )

    fecha_reserva = (
        date.today().isoformat()
    )

    reserva = Reserva(
        cliente=usuario[0],
        paquete=id_paquete,
        fecha_reserva=fecha_reserva,
        cantidad_personas=cantidad_personas,
        total=total
    )

    id_reserva = registrar_reserva(
        reserva
    )

    print(
        "\n¡Reserva realizada correctamente!"
    )

    print(
        f"Número de reserva: {id_reserva}"
    )

    print(
        f"Personas: {cantidad_personas}"
    )

    print(
        f"Total: ${total:,.0f}"
    )


def ver_historial(usuario):

    print(
        "\n=== HISTORIAL DE RESERVAS ==="
    )

    reservas = listar_reservas_cliente(
        usuario[0]
    )

    if not reservas:

        print(
            "No tiene reservas registradas."
        )
        return

    for reserva in reservas:

        print(
            "\n-----------------------------"
        )

        print(
            f"Reserva: {reserva[0]}"
        )

        print(
            f"Paquete: {reserva[2]}"
        )

        print(
            f"Salida: {reserva[3]}"
        )

        print(
            f"Regreso: {reserva[4]}"
        )

        print(
            f"Fecha reserva: {reserva[5]}"
        )

        print(
            f"Personas: {reserva[6]}"
        )

        print(
            f"Total: ${reserva[7]:,.0f}"
        )


# ==========================================================
# MENÚ ADMINISTRADOR
# ==========================================================

def menu_administrador(usuario):

    while True:

        print(
            "\n================================"
        )

        print(
            "       MENÚ ADMINISTRADOR"
        )

        print(
            "================================"
        )

        print(
            "1. Gestionar destinos"
        )

        print(
            "2. Gestionar paquetes"
        )

        print(
            "3. Consultar paquetes"
        )

        print(
            "0. Cerrar sesión"
        )

        opcion = input(
            "Seleccione una opción: "
        )

        if opcion == "1":

            administrar_destinos()

        elif opcion == "2":

            administrar_paquetes()

        elif opcion == "3":

            consultar_paquetes()

        elif opcion == "0":

            print(
                "Sesión cerrada."
            )
            break

        else:

            print(
                "Opción no válida."
            )


# ==========================================================
# MENÚ CLIENTE
# ==========================================================

def menu_cliente(usuario):

    while True:

        print(
            "\n================================"
        )

        print(
            "       MENÚ CLIENTE"
        )

        print(
            "================================"
        )

        print(
            "1. Consultar paquetes"
        )

        print(
            "2. Consultar disponibilidad"
        )

        print(
            "3. Realizar reserva"
        )

        print(
            "4. Ver historial de reservas"
        )

        print(
            "0. Cerrar sesión"
        )

        opcion = input(
            "Seleccione una opción: "
        )

        if opcion == "1":

            consultar_paquetes()

        elif opcion == "2":

            consultar_paquetes()

        elif opcion == "3":

            realizar_reserva(usuario)

        elif opcion == "4":

            ver_historial(usuario)

        elif opcion == "0":

            print(
                "Sesión cerrada."
            )
            break

        else:

            print(
                "Opción no válida."
            )


# ==========================================================
# CONFIGURACIÓN INICIAL DEL ADMINISTRADOR
# ==========================================================

def configurar_administrador():

    print(
        "\n=== CONFIGURACIÓN DEL ADMINISTRADOR ==="
    )

    print(
        "Esta opción permite crear la cuenta "
        "administrativa inicial."
    )

    nombre = input("Nombre: ")
    rut = input("RUT: ")
    telefono = input("Teléfono: ")
    correo = input("Correo: ")
    contrasena = input("Contraseña: ")

    try:

        id_admin = crear_administrador(
            nombre,
            rut,
            telefono,
            correo,
            contrasena
        )

        print(
            "\nAdministrador creado correctamente."
        )

        print(
            f"ID administrador: {id_admin}"
        )

    except ValueError as error:

        print(
            f"\nNo fue posible crear "
            f"el administrador: {error}"
        )

    except Exception as error:

        print(
            f"\nError inesperado: {error}"
        )


# ==========================================================
# MENÚ PRINCIPAL
# ==========================================================

def menu_principal():

    crear_base_datos()

    while True:

        print(
            "\n================================"
        )

        print(
            "       VIAJES AVENTURA"
        )

        print(
            "================================"
        )

        print(
            "1. Registrarse"
        )

        print(
            "2. Iniciar sesión"
        )

        if not existe_administrador():

            print(
                "3. Configurar administrador"
            )

        print(
            "0. Salir"
        )

        opcion = input(
            "Seleccione una opción: "
        )

        if opcion == "1":

            menu_registro()

        elif opcion == "2":

            usuario = iniciar_sesion()

            if usuario is not None:

                if es_administrador(usuario):

                    menu_administrador(
                        usuario
                    )

                elif es_cliente(usuario):

                    menu_cliente(
                        usuario
                    )

                else:

                    print(
                        "El usuario tiene un rol "
                        "no reconocido."
                    )

        elif opcion == "3" and not existe_administrador():

            configurar_administrador()

        elif opcion == "0":

            print(
                "\nGracias por utilizar "
                "Viajes Aventura."
            )

            break

        else:

            print(
                "Opción no válida."
            )


if __name__ == "__main__":
    menu_principal()