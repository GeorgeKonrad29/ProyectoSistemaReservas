"""
screens/home_screen.py: Define la pantalla principal (Home Screen) de la aplicación.
Contiene la barra de navegación, la barra lateral de filtros y el área de listado de objetos.
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Importar las utilidades que ahora están en 'utils'
from utils.navbar import Navbar
from utils.sidebar import Sidebar
from utils.item_card import ItemCard
from app_data import get_sample_items

class HomeScreen(ttk.Frame):
    """
    Pantalla principal donde los usuarios pueden ver y buscar objetos para prestar.
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller # Referencia a la instancia de MainApp
        self._create_widgets()
        self._load_items()

        # Opcional: Escuchar el evento cuando esta pantalla sea mostrada
        self.bind("<<ShowScreens>>", self._on_show_screen)

    def _on_show_screen(self, event=None):
        """Método que se ejecuta cuando esta pantalla es mostrada."""
        print("HomeScreen ha sido mostrada.")
        # Aquí puedes actualizar datos, recargar items, etc.
        # self._load_items()

    def _create_widgets(self):
        """
        Crea y empaqueta los widgets específicos de la HomeScreen.
        """
        # Configurar el grid para esta pantalla
        self.grid_rowconfigure(1, weight=1) # Fila para el contenido principal (sidebar + items)
        self.grid_columnconfigure(1, weight=1) # Columna para los items

        # --- Barra de Navegación Superior (ahora vive dentro de HomeScreen) ---
        # Le pasamos 'self' (la HomeScreen) como su padre, y también 'self.app'
        # para que la Navbar pueda llamar a métodos de MainApp si es necesario.
        self.navbar = Navbar(self, controller=self.controller)
        self.navbar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(5, 0))
        # Puedes añadir callbacks específicos de HomeScreen para los botones de la navbar aquí:
        # self.navbar.search_button.config(command=self._apply_filters)

        # --- Contenedor para Sidebar y Área de Contenido ---
        main_content_frame = ttk.Frame(self)
        main_content_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        # --- Barra Lateral de Filtros ---
        self.sidebar = Sidebar(main_content_frame, controller=self.controller)
        self.sidebar.pack(side=LEFT, fill=Y, padx=(0, 10))
        # Enlazar el botón de aplicar filtros del sidebar a un método de HomeScreen
        self.sidebar.apply_filters_btn.config(command=self._apply_filters)

        # --- Área de Listado de Objetos ---
        self.items_frame = ttk.Frame(main_content_frame, bootstyle="secondary")
        self.items_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        # Canvas y Scrollbar para el área de items
        self.items_canvas = ttk.Canvas(self.items_frame)
        self.items_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.items_frame, orient=VERTICAL, command=self.items_canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.items_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.items_canvas.bind('<Configure>', lambda e: self.items_canvas.configure(scrollregion = self.items_canvas.bbox("all")))

        self.inner_items_frame = ttk.Frame(self.items_canvas)
        self.items_canvas.create_window((0, 0), window=self.inner_items_frame, anchor="nw")

        # Configurar el desplazamiento con la rueda del ratón
        self.inner_items_frame.bind('<Enter>', self._bind_mouse_wheel)
        self.inner_items_frame.bind('<Leave>', self._unbind_mouse_wheel)


    def _bind_mouse_wheel(self, event):
        """Asocia el desplazamiento del ratón al canvas."""
        self.items_canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

    def _unbind_mouse_wheel(self, event):
        """Desasocia el desplazamiento del ratón al canvas."""
        self.items_canvas.unbind_all("<MouseWheel>")

    def _on_mouse_wheel(self, event):
        """Maneja el evento de la rueda del ratón para el scroll."""
        self.items_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _load_items(self):
        """
        Carga los objetos de ejemplo y crea una tarjeta para cada uno.
        Aquí es donde integrarías la lógica de filtrado si estuviera implementada.
        """
        # Limpiar cualquier item existente
        for widget in self.inner_items_frame.winfo_children():
            widget.destroy()

        items = get_sample_items() # Esto vendría de app_data.py
        # Aquí puedes aplicar la lógica de filtrado si ya tienes los valores de los filtros
        # For example:
        # filtered_items = self._filter_items(items)

        for item_data in items: # O filtered_items
            ItemCard(
                self.inner_items_frame,
                name=item_data["name"],
                description=item_data["description"],
                status=item_data["status"],
                daily_value=item_data["daily_value"],
                deposit_value=item_data.get("deposit_value"),
                image_path=item_data.get("image_path")
            ).pack(fill=X, padx=5, pady=5)

        # Asegurarse de que el scrollregion se actualice después de añadir items
        self.update_idletasks()
        self.items_canvas.configure(scrollregion=self.items_canvas.bbox("all"))

    def _apply_filters(self):
        """
        Método llamado cuando se aplican filtros o se realiza una búsqueda.
        """
        selected_categories = self.sidebar.get_selected_categories()
        selected_availability = self.sidebar.get_selected_availability()
        selected_type = self.sidebar.get_selected_type()
        search_query = self.navbar.get_search_query() # Obtener la búsqueda de la navbar

        print(f"Aplicando filtros en HomeScreen: Categorías: {selected_categories}, "
              f"Disponibilidad: {selected_availability}, "
              f"Tipo: {selected_type}, Búsqueda: '{search_query}'")

        # Aquí iría la lógica real para filtrar la lista de items y luego recargarla
        # self._load_items_based_on_filters(selected_categories, selected_availability, selected_type, search_query)
        # Por ahora, simplemente recargamos para simular el cambio:
        self._load_items()

    # --- Métodos de Callback para la Navbar ---
    # Estos métodos son llamados por la Navbar, pero su lógica es de HomeScreen.
    # La Navbar pasa el 'app_instance' para que estos métodos puedan llamar
    # a 'show_screen' de MainApp.
    def show_profile_from_home(self):
        """Callback para mostrar el perfil desde la navbar de HomeScreen."""
        self.app.show_screen("profile")

    def show_my_loans_from_home(self):
        """Callback para mostrar mis préstamos desde la navbar de HomeScreen."""
        print("Mostrar mis préstamos desde HomeScreen")
        ttk.Messagebox.showinfo("Mis Préstamos", "Aquí iría la vista de tus préstamos actuales y pasados.")
