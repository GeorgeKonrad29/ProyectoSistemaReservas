import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests
from ttkbootstrap.dialogs import Messagebox


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
            response = requests.post("http://localhost:8000/login", json={
                "email": email,
                "password": password
            })
            response.raise_for_status()  # Lanza un error si la respuesta no es 200
            Messagebox.show_info("Login exitoso", "Éxito")
            # Aquí puedes redirigir a otra pantalla después de un login exitoso
        except requests.exceptions.RequestException as e:
            try: 
                error_message = e.response.json().get("Error desconocido", "Error desconocido")
            except:
                error_message = str(e)
            Messagebox.show_error("Error: ", error_message)
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
            comman=lambda: print("ingresando") # funcion de ingreso
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