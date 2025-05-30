import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from utils.handle_login import handle_login


class LoginScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        form_frame = ttk.Frame(self)
        form_frame.pack(padx=10, pady=10)

        ttk.Label(
            form_frame,
            text="Ingresar",
            font=("Arial", 20, "bold")
        ).grid(row=1, column=1, pady=30)

        # ingresar usuario
        ttk.Label(
            form_frame,
            text="Ingrese su correo"
        ).grid(row=2, column=1, pady=10)
        self.entry_mail = ttk.Entry(form_frame, width=30)
        self.entry_mail.grid(row=3, column=1, pady=5)

        # ingresar contraseñas
        ttk.Label(form_frame, text="Ingrese su contraseña").grid(row=4, column=1, pady=10)
        self.entry_password = ttk.Entry(form_frame, show="*", width=30)
        self.entry_password.grid(row=5, column=1, pady=5)

        self.btn = ttk.Button(
            form_frame,
            text="ingresar",
            bootstyle=SUCCESS,
            comman=lambda: self.login()
        )
        self.btn.grid(row=6, column=1, pady=10)

        self.label_registro = ttk.Label(
            form_frame,
            text="¿No estas registrado?, Crea una cuenta",
            font=("Arial", 10, "bold"), foreground="blue"
        )
        self.label_registro.grid(row=7, column=1, pady=5)
        self.label_registro.bind("<Button-1>", lambda e: self.show_screens("signup"))

    def show_screens(self, name_screen):
        self.controller.show_screens(name_screen)

    def login(self):
        token = handle_login(self.entry_mail.get(), self.entry_password.get())
        if token:
            self.controller.set_access_token(token)
            self.show_screens("home")
