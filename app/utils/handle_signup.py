import aiohttp
import asyncio
import threading
import re
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox


async def get_error_message(exception):
    """Obtiene el mensaje de error del servidor"""
    try:
        response = exception.response
        return (await response.json()).get("error", "Error desconocido")
    except:
        return str(exception)


def show_error(controller, message):
    """Muestra un mensaje de error en el hilo principal"""
    controller.after(0, lambda: Messagebox.show_error(message, "Error"))


def show_success(controller):
    """Muestra mensaje de éxito en el hilo principal"""
    controller.after(0, lambda: Messagebox.show_info(
        "Usuario registrado exitosamente",
        "Registro exitoso"
    ))


def navigate_to_login(controller):
    """Navega a la pantalla de login en el hilo principal"""
    controller.after(0, lambda: controller.show_screens("login"))


def trigger_signup(mail, name, last_name, password, confirmation, controller):
    """Inicia el proceso de registro en un hilo separado"""
    threading.Thread(
        target=lambda: asyncio.run(
            handle_signup_async(
                mail,
                name,
                last_name,
                password,
                confirmation,
                controller)
        )
    ).start()


def is_valid_email(email: str) -> bool:
    """Valida si un email tiene formato correcto"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


def is_secure_password(password: str) -> bool:
    """Verifica si la contraseña cumple con los requisitos de seguridad"""
    if len(password) < 8:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for c in password)
    return has_upper and has_lower and has_digit and has_special


def validate_signup_fields(first_name: str,
                           last_name: str,
                           email: str,
                           password: str,
                           confirmation: str,
                           controller) -> bool:
    """Valida los campos del formulario de registro"""

    # Eliminar espacios extra
    first_name = first_name.strip().replace(" ", "")
    last_name = last_name.strip().replace(" ", "")
    email = email.strip()
    password = password.strip()
    confirmation = confirmation.strip()

    if not all([first_name, last_name, email, password, confirmation]):
        show_error(controller, "Todos los campos son obligatorios")
        return False

    if not first_name.isalpha() and not last_name.isalpha():
        show_error(controller, "El nombre y apellido solo deben contener letras")
        return False

    if len(first_name.split()) < 1 or len(last_name.split()) < 1:
        show_error(controller, "Debe ingresar al menos un nombre y un apellido")
        return False

    if  is_valid_email(email):
        show_error(controller, "El correo no es válido")
        return False

    if not is_secure_password(password):
        show_error(
            controller,
            "La contraseña debe tener al menos 8 caracteres, incluyendo mayúsculas, minúsculas, números y caracteres especiales"
        )
        return False

    if password != confirmation:
        show_error(controller, "Las contraseñas no coinciden")
        return False

    return True


async def handle_signup_async(mail: str,
                              name: str,
                              last_name: str,
                              password: str,
                              confirmation: str,
                              controller):
    """Maneja el registro de forma asíncrona"""

    # Petición asíncrona al servidor
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:8000/signup/",
                json={
                    "correo": mail,
                    "nombres": name,
                    "apellidos": last_name,
                    "contrasenia": password
                }
            ) as response:
                response.raise_for_status()
                show_success(controller)
                navigate_to_login(controller)
    except aiohttp.ClientResponseError as e:
        error_message = await get_error_message(e)
        show_error(controller, f"Error del servidor: {error_message}")
    except Exception as e:
        show_error(controller, f"Error de conexión: {str(e)}")

