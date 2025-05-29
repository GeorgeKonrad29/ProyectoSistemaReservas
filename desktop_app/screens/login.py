import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests
from ttkbootstrap.dialogs import Messagebox
import json # <-- Añade esta importación para manejar JSON manualmente si lo necesitas, aunque para form-urlencoded no hace falta

class LoginScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def handle_login(self):
        email = self.entry_mail.get().strip()
        password = self.entry_password.get().strip()

        if not email or not password:
            Messagebox.show_error("Todos los campos son obligatorios", "Error")
            return

        try:
            # ✅ JSON correcto con claves esperadas por el backend
            login_data = {
                "correo": email,
                "contrasenia": password
            }

            response = requests.post(
                "http://localhost:8000/login",
                json=login_data,  # ✅ Cambiado de data= a json=
                headers={"Content-Type": "application/json"}  # ✅ Cabecera correcta para JSON
            )

            response.raise_for_status()

            login_response_data = response.json()

            Messagebox.show_info("Login exitoso", "Éxito")
            print(f"Respuesta: {login_response_data}")

            self.controller.set_access_token("FAKE_TOKEN")  # Cambia esto si implementas JWT
            self.controller.show_screens("dashboard_screen")

        except requests.exceptions.HTTPError as e:
            error_detail = e.response.json().get("detail", "Error desconocido")
            if e.response.status_code == 400:
                Messagebox.show_error(f"Credenciales incorrectas: {error_detail}", "Error de Login")
            elif e.response.status_code == 401:
                Messagebox.show_error(f"Autenticación fallida: {error_detail}", "Error de Login")
            elif e.response.status_code == 403:
                Messagebox.show_error(f"Acceso denegado: {error_detail}", "Error de Acceso")
            elif e.response.status_code == 422:
                Messagebox.show_error(f"Error de datos enviados (422): {error_detail}", "Error de Login")
            else:
                Messagebox.show_error(f"Error en el servidor: {e.response.status_code} - {error_detail}", "Error")
        except requests.exceptions.ConnectionError:
            Messagebox.show_error("No se pudo conectar al servidor. Verifique la IP o si el servidor está corriendo.", "Error de Conexión")
        except Exception as e:
            Messagebox.show_error(f"Ocurrió un error inesperado: {e}", "Error")

    def create_widgets(self):
        form_frame = ttk.Frame(self)
        form_frame.pack(padx=10, pady=10)

        ttk.Label(form_frame, text="Ingresar", font=("Arial", 20, "bold")).grid(row=1, column=1, pady=30)

        # ingresar usuario
        ttk.Label(form_frame, text="Ingrese su correo").grid(row=2, column=1, pady=10)
        self.entry_mail = ttk.Entry(form_frame, width=30)
        self.entry_mail.grid(row=3, column=1, pady=5)

        # ingresar contraseñas
        ttk.Label(form_frame, text="Ingrese su contraseña").grid(row=4, column=1, pady=10)
        self.entry_password = ttk.Entry(form_frame, show="*", width=30)
        self.entry_password.grid(row=5, column=1, pady=5)

        # boton de ingresar
        self.btn = ttk.Button(
            form_frame,
            text="ingresar",
            bootstyle=SUCCESS,
            command=lambda: self.handle_login() # Corregido: 'comman' a 'command'
        )
        self.btn.grid(row=6, column=1, pady=10)

        self.label_registro = ttk.Label(
            form_frame,
            text="No estas registrado, Crea una cuenta",
            font=("Arial", 10, "bold"), foreground="blue"
        )
        self.label_registro.grid(row=7, column=1, pady=5)
        self.label_registro.bind("<Button-1>", lambda e: self.show_screens("sign_up"))

    def show_screens(self, name_screen):
        self.controller.show_screens(name_screen)