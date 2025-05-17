import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests
from ttkbootstrap.dialogs import Messagebox

class SignUpScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # metodos
        self.create_widgets()

    def handle_signup(self):
        fullname = self.entry_name.get().strip()
        email = self.entry_mail.get().strip()
        password = self.entry_password.get().strip()
        confirmation = self.entry_confirmation.get().strip()
        accept_terms = self.check.instate(['selected'])

        if not fullname or not email or not password or not confirmation:
            Messagebox.show_error("Todos los campos son obligatorios", "Error")
            return
        if password != confirmation:
            Messagebox.show_error("Las contraseñas no coinciden", "Error")
            return
        if not accept_terms:
            Messagebox.show_error("Debes aceptar los términos y condiciones", "Error")
            return
        
        try:
            response = requests.post("http://localhost:8000/signup", json={
                "fullname": fullname,
                "email": email,
                "password": password
            })
            response.raise_for_status()  # Lanza un error si la respuesta no es 200
            Messagebox.show_info("Usuario registrado exitosamente", "Registro exitoso")
            self.controller.show_screens("login") 
        except requests.exceptions.RequestException as e:
            try: 
                error_message = e.response.json().get("Error desconocido", "Error desconocido")
            except:
                error_message = str(e)
            Messagebox.show_error("Error: ", error_message)



    def create_widgets(self):
        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill="x", pady=10)

        # Marco del formulario
        form_frame = ttk.Frame(self)
        form_frame.pack(pady=10, padx=20)

        ttk.Label(form_frame, text="Registro de Usuario", font=("Arial", 20, "bold")).grid(row=0, column=1, sticky="w",  pady=30)
        # nombre
        ttk.Label(form_frame, text="Ingrese su nombre").grid(row=1, column=1, sticky="w", pady=10)
        self.entry_name = ttk.Entry(form_frame, width=30)
        self.entry_name.grid(row=2, column=1, pady=5)

        # correo
        ttk.Label(form_frame, text="Ingrese su correo electronico").grid(row=3, column=1, sticky="w", pady=10)
        self.entry_mail = ttk.Entry(form_frame, width=30)
        self.entry_mail.grid(row=4, column=1, pady=5)

        # ingrese su contraseña
        ttk.Label(form_frame, text="ingrese su contraseña").grid(row=5, column=1, sticky="w", pady=10)
        self.entry_password = ttk.Entry(form_frame, width=30)
        self.entry_password.grid(row=6, column=1, pady=5)

        # confirmacion de contraseña
        ttk.Label(form_frame, text="Confirme su contraseña").grid(row=7, column=1, sticky="w", pady=10)
        self.entry_confirmation = ttk.Entry(form_frame, width=30)
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
            command=self.handle_signup
        )
        self.btn.grid(row=10, column=1, pady=5)
