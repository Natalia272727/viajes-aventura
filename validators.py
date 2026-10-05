from datetime import datetime, date


# ==========================================================
# VALIDACIONES GENERALES
# ==========================================================

def validar_texto(valor, nombre_campo):
    """
    Comprueba que un campo de texto no esté vacío.
    """

    if not isinstance(valor, str):
        raise ValueError(
            f"{nombre_campo} debe ser texto."
        )

    if not valor.strip():
        raise ValueError(
            f"{nombre_campo} no puede estar vacío."
        )

    return True


def validar_costo(costo_base):
    """
    Comprueba que el costo sea numérico y positivo.
    """

    if not isinstance(
        costo_base,
        (int, float)
    ):
        raise ValueError(
            "El costo base debe ser numérico."
        )

    if costo_base <= 0:
        raise ValueError(
            "El costo base debe ser mayor que cero."
        )

    return True


def validar_cupo(cupo_maximo):
    """
    Comprueba que el cupo sea un entero positivo.
    """

    if not isinstance(
        cupo_maximo,
        int
    ):
        raise ValueError(
            "El cupo máximo debe ser un número entero."
        )

    if cupo_maximo <= 0:
        raise ValueError(
            "El cupo máximo debe ser mayor que cero."
        )

    return True


# ==========================================================
# VALIDACIÓN DE FECHAS
# ==========================================================

def convertir_fecha(fecha_texto):
    """
    Convierte una fecha YYYY-MM-DD a objeto date.
    """

    if not isinstance(fecha_texto, str):
        raise ValueError(
            "La fecha debe estar en formato texto."
        )

    try:
        return datetime.strptime(
            fecha_texto,
            "%Y-%m-%d"
        ).date()

    except ValueError:
        raise ValueError(
            "La fecha debe utilizar el formato YYYY-MM-DD."
        )


def validar_fechas(
    fecha_salida,
    fecha_regreso
):
    """
    Comprueba que las fechas sean válidas
    y que el regreso sea posterior a la salida.
    """

    salida = convertir_fecha(
        fecha_salida
    )

    regreso = convertir_fecha(
        fecha_regreso
    )

    if regreso <= salida:
        raise ValueError(
            "La fecha de regreso debe ser posterior "
            "a la fecha de salida."
        )

    return True


def validar_paquete_vigente(fecha_salida):
    """
    Impide realizar reservas para paquetes
    cuya fecha de salida ya haya pasado.
    """

    salida = convertir_fecha(
        fecha_salida
    )

    if salida <= date.today():
        raise ValueError(
            "No se puede reservar un paquete cuya "
            "fecha de salida ya comenzó o pasó."
        )

    return True


# ==========================================================
# VALIDACIÓN DE DESTINOS
# ==========================================================

def validar_destinos_paquete(destinos):
    """
    Comprueba que un paquete tenga entre 2 y 5
    destinos diferentes y disponibles.

    Los destinos recibidos desde el repositorio
    tienen normalmente esta estructura:

        id,
        nombre,
        ubicacion,
        costo_base

    Si además se recibe la columna disponible,
    también se comprueba su estado.
    """

    if not isinstance(destinos, list):
        raise ValueError(
            "Los destinos deben recibirse como una lista."
        )

    cantidad = len(destinos)

    if cantidad < 2:
        raise ValueError(
            "Un paquete debe tener al menos 2 destinos."
        )

    if cantidad > 5:
        raise ValueError(
            "Un paquete puede tener como máximo 5 destinos."
        )

    ids_destinos = []

    for destino in destinos:

        if not isinstance(
            destino,
            (tuple, list)
        ):
            raise ValueError(
                "Los datos de los destinos no son válidos."
            )

        if len(destino) < 4:
            raise ValueError(
                "La información del destino está incompleta."
            )

        id_destino = destino[0]

        if id_destino in ids_destinos:
            raise ValueError(
                "Un paquete no puede contener "
                "destinos repetidos."
            )

        ids_destinos.append(
            id_destino
        )

        # Si el repositorio entrega también
        # la columna disponible, se valida.
        if len(destino) >= 5:

            disponible = destino[4]

            if disponible != 1:
                raise ValueError(
                    "Todos los destinos del paquete "
                    "deben estar disponibles."
                )

    return True


# ==========================================================
# VALIDACIÓN DE RESERVAS
# ==========================================================

def validar_cantidad_personas(
    cantidad_personas
):
    """
    Comprueba que la cantidad de personas
    de una reserva sea válida.
    """

    if not isinstance(
        cantidad_personas,
        int
    ):
        raise ValueError(
            "La cantidad de personas debe ser "
            "un número entero."
        )

    if cantidad_personas <= 0:
        raise ValueError(
            "La cantidad de personas debe ser "
            "mayor que cero."
        )

    return True


def validar_cupos_disponibles(
    cantidad_personas,
    cupos_disponibles
):
    """
    Impide realizar una reserva que supere
    los cupos disponibles.
    """

    if cupos_disponibles is None:
        raise ValueError(
            "No fue posible consultar "
            "los cupos disponibles."
        )

    if cantidad_personas > cupos_disponibles:
        raise ValueError(
            f"La reserva supera los cupos disponibles. "
            f"Solo quedan {cupos_disponibles} cupos."
        )

    return True


# ==========================================================
# VALIDACIÓN DE CLIENTES
# ==========================================================

def validar_rut(rut):
    """
    Validación básica de RUT.
    """

    validar_texto(
        rut,
        "RUT"
    )

    rut_limpio = (
        rut.replace(".", "")
           .replace("-", "")
           .strip()
    )

    if len(rut_limpio) < 2:
        raise ValueError(
            "El RUT ingresado no es válido."
        )

    return True


def validar_correo(correo):
    """
    Validación básica de correo electrónico.
    """

    validar_texto(
        correo,
        "Correo"
    )

    if (
        "@" not in correo
        or "." not in correo.split("@")[-1]
    ):
        raise ValueError(
            "El correo electrónico no es válido."
        )

    return True


def validar_contrasena(contrasena):
    """
    Comprueba requisitos mínimos para una contraseña.
    """

    if not isinstance(
        contrasena,
        str
    ):
        raise ValueError(
            "La contraseña debe ser texto."
        )

    if len(contrasena) < 8:
        raise ValueError(
            "La contraseña debe tener al menos "
            "8 caracteres."
        )

    return True


def validar_cliente(
    nombre,
    rut,
    telefono,
    correo,
    contrasena
):
    """
    Valida los datos necesarios para registrar
    un cliente o administrador.
    """

    validar_texto(
        nombre,
        "Nombre"
    )

    validar_rut(
        rut
    )

    validar_texto(
        telefono,
        "Teléfono"
    )

    validar_correo(
        correo
    )

    validar_contrasena(
        contrasena
    )

    return True


# ==========================================================
# VALIDACIÓN DE ROLES
# ==========================================================

def validar_rol(rol):
    """
    Comprueba que el rol corresponda a uno
    de los roles permitidos.
    """

    roles_permitidos = {
        "cliente",
        "administrador"
    }

    if rol not in roles_permitidos:
        raise ValueError(
            "El rol indicado no es válido."
        )

    return True