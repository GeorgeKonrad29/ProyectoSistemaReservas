# importar librerias para los graficos
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
# importar las pantallas de la app
from screens.signup import SignUpScreen
from screens.home import HomeScreen
from screens.login import LoginScreen
from screens.profile import ProfileScreen
from screens.terms import TermsScreen
from screens.bookings import BookingsScreen
import os
base_app_path = os.path.dirname(__file__)
terms_file_relative_path = os.path.join(
    base_app_path,
    'utils',
    'terms and condition.txt'
)


class MainApp(ttk.Window):
    def __init__(self, theme='darkly', title='Juana'):
        super().__init__(themename=theme)
        self.title(title + "- sistema de resera")
        self.attributes('-fullscreen', True)
        # Contenedor principal para todas las pantallas
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        # atributos
        self.screens = {}
        # metodos
        self.create_screens(terms_file_relative_path)
        self.show_screens("login")
    def set_access_token(self, token):
        """
        Guarda el token de acceso JWT recibido del backend.
        """
        self.access_token = token
        print(f"Token de acceso guardado en MainApp: {self.access_token[:30]}...") # Imprime solo un fragmento
        

    def create_screens(self, terms_filepath):
        screens = {
            "signup": SignUpScreen(self.container, self),
            "login": LoginScreen(self.container, self),
            "bookings": BookingsScreen(self.container, self),
            "home": HomeScreen(self.container, self),
            "profile": ProfileScreen(self.container, self),
            "terms": TermsScreen(self.container, self, terms_filepath)
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
