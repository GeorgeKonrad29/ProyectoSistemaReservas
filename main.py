# Importar librerías
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Importar pantallas (asegúrate de que estos archivos existan)
from desktop_app.screens.user import UserScreen
from desktop_app.screens.login import LoginScreen
from desktop_app.screens.signup import SignupScreen
from desktop_app.screens.config import ConfigScreen
from desktop_app.screens.bookings import BookingsScreen

class MainApp(ttk.Window):
    def __init__(self, theme='darkly', title='Juana'):
        super().__init__(themename=theme)
        self.title(f"{title} - sistema de reserva")  # Título corregido
        self.state("zoomed")
        
        # Configurar contenedor principal
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Diccionario de pantallas
        self.screens = {}
        
        # Inicializar pantallas
        self.create_screens()
        self.show_screen("login")

    def create_screens(self):
        screens = {
            "login": LoginScreen(self.container, self),
            "signup": SignupScreen(self.container, self),  # Añade esta línea
            "user": UserScreen(self.container, self),
            "bookings": BookingsScreen(self.container, self),
            "config": ConfigScreen(self.container, self)
        }
        
        # Registrar pantallas
        for name, screen in screens.items():
            self.screens[name] = screen
            screen.grid(row=0, column=0, sticky="nsew")  # Todas en la misma posición

    def show_screen(self, screen_name):
        # Obtener pantalla y mostrarla
        screen = self.screens.get(screen_name)
        if screen:
            screen.tkraise()  # Método estándar para mostrar frames
            screen.event_generate("<<ScreenShown>>")  # Opcional: evento personalizado

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()