import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import aiohttp
import asyncio
import threading
import re
from ttkbootstrap.dialogs import Messagebox

class SignUpScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def is_valid_email(self, email: str) -> bool:
        """Valida si un email tiene formato correcto"""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def is_secure_password(self, password: str) -> bool:
        """Verifica si la contraseña cumple con los requisitos de seguridad"""
        if len(password) < 8:
            return False
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for c in password)
        return has_upper and has_lower and has_digit and has_special

    async def handle_signup_async(self):
        """Maneja el registro de forma asíncrona"""
        fullname = self.entry_name.get().strip()
        email = self.entry_mail.get().strip()
        password = self.entry_password.get().strip()
        confirmation = self.entry_confirmation.get().strip()
        accept_terms = self.check.instate(['selected'])

        # Validación de campos
        if not all([fullname, email, password, confirmation]):
            self.show_error("Todos los campos son obligatorios")
            return

        if not fullname.replace(" ", "").isalpha():
            self.show_error("El nombre solo debe contener letras")
            return

        if len(fullname.split()) < 2:
            self.show_error("Debe contener al menos un nombre y un apellido")
            return

        if not self.is_valid_email(email):
            self.show_error("El correo no es válido")
            return

        if not self.is_secure_password(password):
            self.show_error("La contraseña debe tener al menos 8 caracteres, incluyendo mayúsculas, minúsculas, números y caracteres especiales")
            return

        if password != confirmation:
            self.show_error("Las contraseñas no coinciden")
            return

        if not accept_terms:
            self.show_error("Debes aceptar los términos y condiciones")
            return

        # Petición asíncrona al servidor
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    
                    "http://localhost:8000/signup",  # Cambia a tu URL real
                    #"http://192.168.0.11:8000/signup",
                    json={
                        "correo": email,
                        "nombres": fullname.split()[0],
                        "apellidos": " ".join(fullname.split()[1:]),
                        "contrasenia": password
                    }
                ) as response:
                    response.raise_for_status()
                    self.show_success()
                    self.navigate_to_login()
        except aiohttp.ClientResponseError as e:
            error_message = await self.get_error_message(e)
            self.show_error(f"Error del servidor: {error_message}")
        except Exception as e:
            self.show_error(f"Error de conexión: {str(e)}")

    async def get_error_message(self, exception):
        """Obtiene el mensaje de error del servidor"""
        try:
            response = exception.response
            return (await response.json()).get("error", "Error desconocido")
        except:
            return str(exception)

    def show_error(self, message):
        """Muestra un mensaje de error en el hilo principal"""
        self.controller.after(0, lambda: Messagebox.show_error(message, "Error"))

    def show_success(self):
        """Muestra mensaje de éxito en el hilo principal"""
        self.controller.after(0, lambda: Messagebox.show_info(
            "Usuario registrado exitosamente", 
            "Registro exitoso"
        ))

    def navigate_to_login(self):
        """Navega a la pantalla de login en el hilo principal"""
        self.controller.after(0, lambda: self.controller.show_screens("login"))

    def trigger_signup(self):
        """Inicia el proceso de registro en un hilo separado"""
        threading.Thread(
            target=asyncio.run,
            args=(self.handle_signup_async(),)
        ).start()

    def create_widgets(self):
        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill="x", pady=10)

        # Marco del formulario
        form_frame = ttk.Frame(self)
        form_frame.pack(pady=10, padx=20)

        ttk.Label(form_frame, text="Registro de Usuario", font=("Arial", 20, "bold")).grid(row=0, column=1, sticky="w",  pady=30)
        # nombre
        ttk.Label(form_frame, text="Ingrese su nombre y apellido").grid(row=1, column=1, sticky="w", pady=10)
        self.entry_name = ttk.Entry(form_frame, width=30)
        self.entry_name.grid(row=2, column=1, pady=5)

        # correo
        ttk.Label(form_frame, text="Ingrese su correo electronico").grid(row=3, column=1, sticky="w", pady=10)
        self.entry_mail = ttk.Entry(form_frame, width=30)
        self.entry_mail.grid(row=4, column=1, pady=5)

        # ingrese su contraseña
        ttk.Label(form_frame, text="ingrese su contraseña").grid(row=5, column=1, sticky="w", pady=10)
        self.entry_password = ttk.Entry(form_frame,show="*", width=30)
        self.entry_password.grid(row=6, column=1, pady=5)

        # confirmacion de contraseña
        ttk.Label(form_frame, text="Confirme su contraseña").grid(row=7, column=1, sticky="w", pady=10)
        self.entry_confirmation = ttk.Entry(form_frame, show="*", width=30)
        self.entry_confirmation.grid(row=8, column=1, pady=5)

        # aceptar terminos y condiciones
        self.check = ttk.Checkbutton(
            form_frame,
            text="acepto los terminos y condiciones",
            bootstyle="round-toggle",
            variable=ttk.BooleanVar(value=False)
        )
        self.check.grid(row=9, column=1, pady=5)

        # Registrarse
        self.btn = ttk.Button(
            form_frame,
            text="Registrarme",
            bootstyle=SUCCESS,
            command=self.trigger_signup
        )
        self.btn.grid(row=10, column=1, pady=5)
