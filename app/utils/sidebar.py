import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class Sidebar(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bootstyle="secondary")
        self.controller = controller
        self._create_widgets()
        self._setup_filter_variables()

    def _setup_filter_variables(self):
        """Inicializa las variables para los valores de los filtros."""
        self.selected_categories = []
        self.selected_availability = []
        self.selected_type = ttk.StringVar(value="Objeto")

    def _create_widgets(self):
        """
        Crea y organiza los widgets de la barra lateral.
        """
        filter_title = ttk.Label(self, text="FILTROS", font=("Helvetica", 12, "bold"), bootstyle="light")
        filter_title.pack(padx=10, pady=(15, 10), anchor=W)

        # --- Filtro por Categorías ---
        category_frame = ttk.LabelFrame(self, text="Categorías", bootstyle="light")
        category_frame.pack(fill=X, padx=10, pady=5)
        self.category_checkboxes = {}
        categories = ["Microfonos", "Parlantes", "Zonas Culturales", "Instrumentos", "Cabinas"]
        for cat in categories:
            var = ttk.BooleanVar(value=False)
            chk = ttk.Checkbutton(category_frame, text=cat, variable=var, bootstyle="toggle,round-toggle")
            chk.pack(anchor=W, pady=2, padx=5)
            self.category_checkboxes[cat] = var

        # --- Filtro por Disponibilidad ---
        availability_frame = ttk.LabelFrame(self, text="Disponibilidad", bootstyle="light")
        availability_frame.pack(fill=X, padx=10, pady=5)
        self.availability_checkboxes = {}
        availability_options = ["Disponible Ahora", "En Préstamo"]
        for avail in availability_options:
            var = ttk.BooleanVar(value=False)
            chk = ttk.Checkbutton(availability_frame, text=avail, variable=var, bootstyle="toggle,round-toggle")
            chk.pack(anchor=W, pady=2, padx=5)
            self.availability_checkboxes[avail] = var

        # --- Filtro por Tipo de Bien (Escenario u Objeto) ---
        type_frame = ttk.LabelFrame(self, text="Tipo de Bien", bootstyle="light")
        type_frame.pack(fill=X, padx=10, pady=5)

        self.object_radio = ttk.Radiobutton(type_frame, text="Objeto", variable=self.get_selected_type, value="Objeto", bootstyle="info,round-toggle")
        self.object_radio.pack(anchor=W, pady=2, padx=5)

        self.scenario_radio = ttk.Radiobutton(type_frame, text="Escenario", variable=self.get_selected_type, value="Escenario", bootstyle="info,round-toggle")
        self.scenario_radio.pack(anchor=W, pady=2, padx=5)

        # --- Botón para Aplicar Filtros ---
        self.apply_filters_btn = ttk.Button(self, text="Aplicar Filtros", bootstyle="success")
        self.apply_filters_btn.pack(fill=X, padx=10, pady=15)
        # El comando se configurará en HomeScreen, ya que HomeScreen es el que gestiona la carga de ítems.

    def get_selected_categories(self):
        """Retorna una lista de las categorías seleccionadas."""
        return [cat for cat, var in self.category_checkboxes.items() if var.get()]

    def get_selected_availability(self):
        """Retorna una lista de las opciones de disponibilidad seleccionadas."""
        return [avail for avail, var in self.availability_checkboxes.items() if var.get()]

    def get_selected_type(self):
        """Retorna el tipo de bien seleccionado (Objeto o Escenario)."""
        return self.selected_type.get()
