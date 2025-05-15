import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

class LoginScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure_style()
        self.create_widgets()
        
    def configure_style(self):
        # Configuraciones específicas para esta pantalla
        self.style = ttk.Style()
        self.style.configure('Login.TButton', font=('Arial', 12))
        self.style.configure('LoginTitle.TLabel', font=('Arial', 16, 'bold'))
        
    def create_widgets(self):
        # Contenedor principal
        container = ttk.Frame(self, padding=20)
        container.pack(expand=True, fill=BOTH)
        
        # Título
        ttk.Label(
            container, 
            text="Iniciar Sesión", 
            style='LoginTitle.TLabel'
        ).grid(row=0, column=0, columnspan=2, pady=20)

        # Campo de usuario
        ttk.Label(container, text="Usuario:").grid(row=1, column=0, padx=5, pady=5, sticky=E)
        self.username_entry = ttk.Entry(container)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5, sticky=EW)

        # Campo de contraseña
        ttk.Label(container, text="Contraseña:").grid(row=2, column=0, padx=5, pady=5, sticky=E)
        self.password_entry = ttk.Entry(container, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5, sticky=EW)

        # Botón de ingreso
        login_btn = ttk.Button(
            container,
            text="Ingresar",
            style='Login.TButton',
            command=self.handle_login,
            bootstyle=SUCCESS
        )
        login_btn.grid(row=3, column=0, columnspan=2, pady=20, sticky=EW)

        # Enlace de registro
        ttk.Label(container, text="¿No tienes cuenta?", foreground='gray').grid(row=4, column=0, columnspan=2)
        ttk.Button(
            container,
            text="Regístrate aquí",
            command=lambda: self.controller.show_screen("signup"),
            bootstyle=LINK
        ).grid(row=5, column=0, columnspan=2)

        # Configurar grid
        container.grid_columnconfigure(1, weight=1)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return
            
        # Lógica de autenticación (simulada)
        if username == "admin" and password == "password":
            self.controller.show_screen("user")  # Cambiar a pantalla principal
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")