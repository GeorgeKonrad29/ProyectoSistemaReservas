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
            # --- CAMBIOS AQUÍ ---
            # 1. Cambiar la URL a /token
            # 2. Cambiar 'json=' por 'data=' y usar un diccionario para form-urlencoded
            # 3. Establecer Content-Type explícitamente (requests lo hace automáticamente con 'data', pero es buena práctica)

            # Datos para enviar en formato form-urlencoded
            login_data = {
                "username": email, # FastAPI espera 'username' para el correo
                "password": password
            }

            response = requests.post(
                "http://192.168.0.11:8000/login", # ¡CAMBIADO de /login a /token!
                data=login_data, # ¡CAMBIADO de json= a data=! requests lo codificará como form-urlencoded
                headers={"Content-Type": "application/x-www-form-urlencoded"} # Asegura el tipo de contenido
            )
            # --- FIN DE CAMBIOS ---

            response.raise_for_status()  # Lanza un error si la respuesta no es 200 (ej: 400, 401, 403)

            # Si el login es exitoso, la respuesta contendrá el token
            login_response_data = response.json()
            access_token = login_response_data.get("access_token")
            token_type = login_response_data.get("token_type")

            Messagebox.show_info("Login exitoso", "Éxito")
            print(f"Token de acceso: {access_token}") # Para depuración
            # Aquí puedes guardar el access_token y token_type para futuras peticiones
            # y redirigir a otra pantalla después de un login exitoso
            self.controller.set_access_token(access_token) # Si tienes una función para guardar el token en el controller
            self.controller.show_screens("dashboard_screen") # Ejemplo de redirección

        except requests.exceptions.HTTPError as e:
            error_detail = e.response.json().get("detail", "Error desconocido")
            if e.response.status_code == 400:
                Messagebox.show_error(f"Credenciales incorrectas: {error_detail}", "Error de Login")
            elif e.response.status_code == 401: # FastAPI podría devolver 401 si el token falla
                 Messagebox.show_error(f"Autenticación fallida: {error_detail}", "Error de Login")
            elif e.response.status_code == 403: # Esto sería si implementaras bloqueo de cuenta
                Messagebox.show_error(f"Acceso denegado: {error_detail}", "Error de Acceso")
            elif e.response.status_code == 422: # Error de validación de FastAPI
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