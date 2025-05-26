import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class Navbar(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._create_widgets()

    def _create_widgets(self):
        # --- Lado Izquierdo: Logo ---
        logo_label = ttk.Label(self, text="Juana- prestamos", font=("Helvetica", 16, "bold"))
        logo_label.pack(side=LEFT, padx=(15, 20), pady=10)

        # --- Centro: Barra de Búsqueda ---
        search_frame = ttk.Frame(self, bootstyle="secondary")
        search_frame.pack(side=LEFT, padx=10, pady=10, fill=X, expand=True)

        self.search_entry = ttk.Entry(search_frame, bootstyle="light")
        self.search_entry.pack(side=LEFT, fill=X, expand=True, padx=5, pady=5)
        # La búsqueda ahora es gestionada por la HomeScreen, que llama a _apply_filters
        self.search_entry.bind("<Return>", lambda e: self.master._apply_filters())

        self.search_button = ttk.Button(search_frame, text="Buscar", command=self.master._apply_filters, bootstyle="info")
        self.search_button.pack(side=RIGHT, padx=5, pady=5)

        # --- Lado Derecho: Botones de Navegación ---
        nav_buttons_frame = ttk.Frame(self, bootstyle="primary")
        nav_buttons_frame.pack(side=RIGHT, padx=15, pady=10)

        # Los comandos de estos botones ahora llaman a métodos de la HomeScreen
        self.profile_btn = ttk.Button(
            nav_buttons_frame,
            text="Mi Perfil",
            command=lambda: self.show_screens("profile"),
        )
        self.profile_btn.pack(side=LEFT, padx=5)

        self.my_loans_btn = ttk.Button(
            nav_buttons_frame,
            text="Mis Préstamos",
            command=lambda: self.show_screens("bookings"),
        )
        self.my_loans_btn.pack(side=LEFT, padx=5)

        self.notifications_btn = ttk.Button(
            nav_buttons_frame,
            text="Notificaciones",
        )
        self.notifications_btn.pack(side=LEFT, padx=5)

    def get_search_query(self):
        """Retorna el texto actual de la barra de búsqueda."""
        return self.search_entry.get()

    def show_screens(self, name_screen):
        self.controller.show_screens(name_screen)
