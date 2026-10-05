import hashlib
import hmac
import secrets

from cliente import Cliente
from cliente_repository import (
    buscar_cliente_por_correo,
    existe_cliente,
    existe_administrador,
    registrar_cliente
)
from validators import validar_cliente


def generar_hash_contrasena(contrasena):
    """
    Genera un hash seguro utilizando scrypt.
    La contraseña original nunca se almacena.
    """

    if not isinstance(contrasena, str):
        raise ValueError("La contraseña debe ser texto.")

    if not contrasena:
        raise ValueError("La contraseña no puede estar vacía.")

    salt = secrets.token_bytes(16)

    hash_contrasena = hashlib.scrypt(
        contrasena.encode("utf-8"),
        salt=salt,
        n=16384,
        r=8,
        p=1
    )

    return f"{salt.hex()}:{hash_contrasena.hex()}"


def verificar_contrasena(contrasena, contrasena_hash):
    """
    Verifica una contraseña contra el hash almacenado.
    """

    if not isinstance(contrasena, str):
        return False

    if not isinstance(contrasena_hash, str):
        return False

    try:
        salt_hex, hash_hex = contrasena_hash.split(":")

        salt = bytes.fromhex(salt_hex)
        hash_original = bytes.fromhex(hash_hex)

    except (ValueError, TypeError):
        return False

    hash_ingresado = hashlib.scrypt(
        contrasena.encode("utf-8"),
        salt=salt,
        n=16384,
        r=8,
        p=1
    )

    return hmac.compare_digest(
        hash_ingresado,
        hash_original
    )


def autenticar_usuario(correo, contrasena):
    """
    Autentica un usuario mediante correo y contraseña.
    """

    usuario = buscar_cliente_por_correo(correo)

    if usuario is None:
        return None

    contrasena_hash = usuario[5]

    if verificar_contrasena(contrasena, contrasena_hash):
        return usuario

    return None


def es_administrador(usuario):
    """
    Determina si el usuario tiene rol administrador.
    """

    if usuario is None:
        return False

    return usuario[6] == "administrador"


def es_cliente(usuario):
    """
    Determina si el usuario tiene rol cliente.
    """

    if usuario is None:
        return False

    return usuario[6] == "cliente"


def registrar_nuevo_cliente(
    nombre,
    rut,
    telefono,
    correo,
    contrasena
):
    """
    Registra una cuenta normal de cliente.
    Nunca permite escoger el rol administrador.
    """

    validar_cliente(
        nombre,
        rut,
        telefono,
        correo,
        contrasena
    )

    if existe_cliente(correo, rut):
        raise ValueError(
            "Ya existe un cliente con ese correo o RUT."
        )

    hash_contrasena = generar_hash_contrasena(contrasena)

    cliente = Cliente(
        nombre=nombre,
        rut=rut,
        telefono=telefono,
        correo=correo,
        contrasena_hash=hash_contrasena,
        rol="cliente"
    )

    return registrar_cliente(cliente)


def crear_administrador(
    nombre,
    rut,
    telefono,
    correo,
    contrasena
):
    """
    Crea la cuenta administrativa inicial.

    Esta función se utiliza durante la configuración inicial
    y no forma parte del registro público de clientes.
    """

    if existe_administrador():
        raise ValueError(
            "Ya existe un administrador registrado."
        )

    validar_cliente(
        nombre,
        rut,
        telefono,
        correo,
        contrasena
    )

    if existe_cliente(correo, rut):
        raise ValueError(
            "Ya existe un usuario con ese correo o RUT."
        )

    hash_contrasena = generar_hash_contrasena(contrasena)

    administrador = Cliente(
        nombre=nombre,
        rut=rut,
        telefono=telefono,
        correo=correo,
        contrasena_hash=hash_contrasena,
        rol="administrador"
    )

    return registrar_cliente(administrador)