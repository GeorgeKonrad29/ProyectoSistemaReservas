import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class ProfileScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._create_widgets()

        # Opcional: Escuchar el evento cuando esta pantalla sea mostrada
        self.bind("<<ShowScreens>>", self._on_show_screen)

    def _on_show_screen(self, event=None):
        """Método que se ejecuta cuando esta pantalla es mostrada."""
        print("ProfileScreen ha sido mostrada.")
        # Aquí puedes cargar los datos del perfil del usuario, etc.

    def _create_widgets(self):
        """Crea y organiza los widgets de la pantalla de perfil."""
        # Centrar el contenido en la pantalla
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        profile_frame = ttk.Frame(self, bootstyle="secondary", padding=30)
        profile_frame.grid(row=1, column=1, sticky="nsew")

        ttk.Label(
            profile_frame,
            text="Mi Perfil",
            font=("Arial", 16, "bold"),
            bootstyle="primary"
        ).pack(pady=10)

        ttk.Label(
            profile_frame,
            text="Nombre de Usuario: John Doe"
        ).pack(pady=5)
        ttk.Label(
            profile_frame,
            text="Email: john.doe@example.com"
        ).pack(pady=5)
        ttk.Label(
            profile_frame,
            text="Préstamos Activos: 2"
        ).pack(pady=5)
        ttk.Label(
            profile_frame,
            text="Objetos Prestados: 5"
        ).pack(pady=5)

        ttk.Button(
            profile_frame,
            text="Editar Perfil",
            bootstyle="info"
        ).pack(pady=10)
        ttk.Button(
            profile_frame,
            text="Cerrar Sesión",
            bootstyle="danger"
        ).pack(pady=5)

        back_button = ttk.Button(
            profile_frame,
            text="Volver al Inicio",
            bootstyle="link",
            command=lambda: self.controller.show_screen("home")
        )
        back_button.pack(pady=20)

