# desktop_app/screens/signup.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

class SignupScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure_style()
        self.create_widgets()
        
    def configure_style(self):
        self.style = ttk.Style()
        self.style.configure('Signup.TEntry', font=('Arial', 12))
        self.style.configure('SignupTitle.TLabel', font=('Arial', 16, 'bold'))
        
    def create_widgets(self):
        container = ttk.Frame(self, padding=20)
        container.pack(expand=True, fill=BOTH)
        
        # Título
        ttk.Label(
            container,
            text="Registro",
            style='SignupTitle.TLabel'
        ).grid(row=0, column=0, columnspan=2, pady=20)

        # Campos del formulario
        fields = [
            ("Nombre completo:", 1),
            ("Correo electrónico:", 2),
            ("Usuario:", 3),
            ("Contraseña:", 4),
            ("Confirmar contraseña:", 5)
        ]
        
        self.entries = {}
        for text, row in fields:
            ttk.Label(container, text=text).grid(row=row, column=0, padx=5, pady=5, sticky=E)
            show = "*" if "contraseña" in text.lower() else ""
            entry = ttk.Entry(container, show=show, style='Signup.TEntry')
            entry.grid(row=row, column=1, padx=5, pady=5, sticky=EW)
            self.entries[text] = entry

        # Botón de registro
        ttk.Button(
            container,
            text="Registrarse",
            command=self.handle_signup,
            bootstyle=SUCCESS
        ).grid(row=6, column=0, columnspan=2, pady=20, sticky=EW)

        # Enlace de inicio de sesión
        ttk.Label(container, text="¿Ya tienes cuenta?", foreground='gray').grid(
            row=7, column=0, columnspan=2)
        ttk.Button(
            container,
            text="Inicia sesión aquí",
            command=lambda: self.controller.show_screen("login"),
            bootstyle=LINK
        ).grid(row=8, column=0, columnspan=2)

        # Configurar grid
        container.grid_columnconfigure(1, weight=1)

    def handle_signup(self):
        values = {key: entry.get().strip() for key, entry in self.entries.items()}
        
        # Validación de campos
        for field, value in values.items():
            if not value:
                messagebox.showerror("Error", f"El campo '{field[:-1]}' es obligatorio")
                return
                
        if values["Contraseña:"] != values["Confirmar contraseña:"]:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
            
        # Lógica de registro (simulada)
        messagebox.showinfo("Éxito", "Registro exitoso. Ahora puedes iniciar sesión")
        self.controller.show_screen("login")