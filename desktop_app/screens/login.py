import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class LoginScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

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

