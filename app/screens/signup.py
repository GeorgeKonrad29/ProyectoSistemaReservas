import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class SignUpScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # metodos
        self.create_widgets()

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

        # apellido
        ttk.Label(form_frame, text="ingrese su apellido").grid(row=3, column=1, sticky="w", pady=10)
        self.entry_last_name = ttk.Entry(form_frame, width=30)
        self.entry_last_name.grid(row=4, column=1, pady=5)
        # correo
        ttk.Label(form_frame, text="Ingrese su correo electronico").grid(row=5, column=1, sticky="w", pady=10)
        self.entry_mail = ttk.Entry(form_frame, width=30)
        self.entry_mail.grid(row=6, column=1, pady=5)

        # ingrese su contraseña
        ttk.Label(form_frame, text="ingrese su contraseña").grid(row=7, column=1, sticky="w", pady=10)
        self.entry_password = ttk.Entry(form_frame, width=30)
        self.entry_password.grid(row=8, column=1, pady=5)

        # confirmacion de contraseña
        ttk.Label(form_frame, text="Confirme su contraseña").grid(row=9, column=1, sticky="w", pady=10)
        self.entry_confirmation = ttk.Entry(form_frame, width=30)
        self.entry_confirmation.grid(row=10, column=1, pady=5)

        # aceptar terminos y condiciones
        terms_button = ttk.Button(
            self,
            text="Ver Términos y Condiciones",
            command=self._navigate_to_terms,
            bootstyle=INFO
        )
        terms_button.pack(pady=10)

        ttk.Label(
            form_frame,
            text="Al registrase acepta los terminos y condicions"
        ).grid(row=12, column=1, pady=10)



        # Registrarse
        self.btn = ttk.Button(
            form_frame,
            text="Registrarme",
            bootstyle=SUCCESS,
            command=lambda: print("aja") # funcion para registrarse
        )
        self.btn.grid(row=13, column=1, pady=5)

    def _navigate_to_terms(self):
        """Navigates to the 'terms' screen using the main controller."""
        self.controller.show_screens("terms")
