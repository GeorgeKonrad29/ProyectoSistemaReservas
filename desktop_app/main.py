# importar librerias para los graficos
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
# importar las pantallas de la app
from screens.signup import SignUpScreen
# from screens.user import UserScreen
from screens.login import LoginScreen
# from screens.config import ConfigScreen
# from screens.bookings import BookingsScreen


class MainApp(ttk.Window):
    def __init__(self, theme='darkly', title='Juana'):
        super().__init__(themename=theme)
        self.title(title + "- sistema de resera")
        # self.state("zoomed")
        # Contenedor principal para todas las pantallas
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        # atributos
        self.screens = {}
        # metodos
        self.create_screens()
        self.show_screens("login")

    def set_access_token(self, token):
        """
        Guarda el token de acceso JWT recibido del backend.
        """
        self.access_token = token
        print(f"Token de acceso guardado en MainApp: {self.access_token[:30]}...") # Imprime solo un fragmento
    

    def create_screens(self):
        screens = {
            "sign_up": SignUpScreen(self.container, self),
            "login": LoginScreen(self.container, self),
            # "user": UserScreen(self.container, self),
            # "bookings": BookingsScreen(self.container, self),
            # "config": ConfigScreen(self.container, self)
        }
        for name, screen in screens.items():
            self.screens[name] = screen
            screen.grid(row=0, column=0, sticky="nsew")

    def show_screens(self, name_screen):
        screen = self.screens[name_screen]
        screen.tkraise()
        screen.event_generate("<<ShowScreens>>")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()