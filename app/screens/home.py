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
import requests
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
        Carga los objetos de escenario desde la API de FastAPI y crea una tarjeta para cada uno.
        """
        # Limpiar cualquier item existente antes de cargar nuevos
        for widget in self.inner_items_frame.winfo_children():
            widget.destroy()

        # Define la URL de tu endpoint de FastAPI
        api_url = "http://192.168.0.14:8000/escenarios?skip=0&limit=100" # Increased limit for more items

        scenarios = []
        try:
            # Realiza la petición GET a tu endpoint de FastAPI
            response = requests.get(api_url, headers={"accept": "application/json"})
            response.raise_for_status()  # Lanza un HTTPError para respuestas de error (4xx o 5xx)

            # Parsea la respuesta JSON
            scenarios = response.json()

            # Asegúrate de que la respuesta sea una lista, como se espera
            if not isinstance(scenarios, list):
                print(f"Advertencia: La respuesta de la API no fue una lista. Recibido: {scenarios}")
                scenarios = [] # Asume una lista vacía para evitar errores
            
        except requests.exceptions.ConnectionError as e:
            print(f"Error de conexión a la API: Asegúrate de que FastAPI esté corriendo en {api_url}. Detalles: {e}")
            # Puedes mostrar un mensaje al usuario en la UI aquí
        except requests.exceptions.Timeout as e:
            print(f"La petición a la API excedió el tiempo límite. Detalles: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error al realizar la petición GET a la API. Detalles: {e}")
        except ValueError as e: # Catch JSON decoding errors
            print(f"Error al parsear la respuesta JSON de la API. Detalles: {e}")

        # Recorre la lista de escenarios y crea una ItemCard para cada uno
        for scenario_data in scenarios:
            # Mapeo de los datos de la API a los argumentos de ItemCard
            card_name = scenario_data.get("Direccion", "Dirección Desconocida")
            
            # Construye una descripción combinando Capacidad y Precio
            capacidad = scenario_data.get("Capacidad", "N/A")
            precio = scenario_data.get("Precio", "N/A")
            card_description = f"Capacidad: {capacidad}, Precio: ${precio}"
            
            # Mapea el estado booleano 'Activo' a un string descriptivo
            activo = scenario_data.get("Activo", False)
            card_status = "Activo" if activo else "Inactivo"
            
            # Asumiendo que 'Precio' de la API es tu 'daily_value'
            card_daily_value = scenario_data.get("Precio", 0.0)
            
            # 'deposit_value' e 'image_path' no están en tu ejemplo de respuesta.
            # Los manejamos con valores por defecto o None.
            card_deposit_value = scenario_data.get("deposit_value", 0.0) # Si la API lo agrega en el futuro
            card_image_path = scenario_data.get("image_path", None) # Si la API lo agrega en el futuro

            ItemCard(
                self.inner_items_frame,
                name=card_name,
                description=card_description,
                status=card_status,
                daily_value=float(card_daily_value), # Asegura que sea flotante
                deposit_value=float(card_deposit_value), # Asegura que sea flotante
                image_path=card_image_path
            ).pack(fill=X, padx=5, pady=5)

        # Asegurarse de que el scrollregion se actualice después de añadir items
        # Esto es crucial para que el scrollbar funcione correctamente
        self.master.update_idletasks() # Actualiza los widgets para que sus tamaños se calculen
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
