import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from utils.item_card import ItemCard # Reutilizamos ItemCard
from app_data import get_user_bookings # Nueva función para obtener reservas


class BookingsScreen(ttk.Frame):
    """
    Pantalla que muestra las reservas activas del usuario, divididas en objetos y escenarios.
    """
    def __init__(self, parent_container, app_instance, **kwargs):
        super().__init__(parent_container, **kwargs)
        self.app = app_instance # Referencia a la instancia de MainApp
        self._create_widgets()

        # Opcional: Escuchar el evento cuando esta pantalla sea mostrada
        self.bind("<<ShowScreens>>", self._on_show_screen)

    def _on_show_screen(self, event=None):
        """Método que se ejecuta cuando esta pantalla es mostrada."""
        print("BookingsScreen ha sido mostrada. Cargando reservas...")
        self._load_bookings()

    def _create_widgets(self):
        """
        Crea y organiza los widgets para la pantalla de reservas.
        """
        # --- Título de la Pantalla ---
        title_label = ttk.Label(self, text="Mis Reservas Activas", font=("Helvetica", 18, "bold"), bootstyle="primary")
        title_label.pack(pady=(20, 15), anchor=CENTER)

        # --- Contenedor para las dos secciones (Objetos y Escenarios) ---
        sections_frame = ttk.Frame(self)
        sections_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # Configurar las columnas del frame para que se expandan por igual
        sections_frame.grid_columnconfigure(0, weight=1)
        sections_frame.grid_columnconfigure(1, weight=1)

        # --- Sección de Objetos ---
        objects_frame = ttk.LabelFrame(sections_frame, text="Objetos Reservados", bootstyle="info")
        objects_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=5)
        objects_frame.grid_rowconfigure(0, weight=1)
        objects_frame.grid_columnconfigure(0, weight=1)

        self.objects_canvas = ttk.Canvas(objects_frame)
        self.objects_canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.objects_scrollbar = ttk.Scrollbar(objects_frame, orient=VERTICAL, command=self.objects_canvas.yview)
        self.objects_scrollbar.pack(side=RIGHT, fill=Y)
        self.objects_canvas.configure(yscrollcommand=self.objects_scrollbar.set)
        self.objects_canvas.bind('<Configure>', lambda e: self.objects_canvas.configure(scrollregion = self.objects_canvas.bbox("all")))
        self.inner_objects_frame = ttk.Frame(self.objects_canvas)
        self.objects_canvas.create_window((0, 0), window=self.inner_objects_frame, anchor="nw")
        self.inner_objects_frame.bind('<Enter>', lambda e: self._bind_mouse_wheel(self.objects_canvas))
        self.inner_objects_frame.bind('<Leave>', self._unbind_mouse_wheel)


        # --- Sección de Escenarios ---
        scenarios_frame = ttk.LabelFrame(sections_frame, text="Escenarios Reservados", bootstyle="warning")
        scenarios_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=5)
        scenarios_frame.grid_rowconfigure(0, weight=1)
        scenarios_frame.grid_columnconfigure(0, weight=1)

        self.scenarios_canvas = ttk.Canvas(scenarios_frame)
        self.scenarios_canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.scenarios_scrollbar = ttk.Scrollbar(scenarios_frame, orient=VERTICAL, command=self.scenarios_canvas.yview)
        self.scenarios_scrollbar.pack(side=RIGHT, fill=Y)
        self.scenarios_canvas.configure(yscrollcommand=self.scenarios_scrollbar.set)
        self.scenarios_canvas.bind('<Configure>', lambda e: self.scenarios_canvas.configure(scrollregion = self.scenarios_canvas.bbox("all")))
        self.inner_scenarios_frame = ttk.Frame(self.scenarios_canvas)
        self.scenarios_canvas.create_window((0, 0), window=self.inner_scenarios_frame, anchor="nw")
        self.inner_scenarios_frame.bind('<Enter>', lambda e: self._bind_mouse_wheel(self.scenarios_canvas))
        self.inner_scenarios_frame.bind('<Leave>', self._unbind_mouse_wheel)

        # --- Botón para volver al Home ---
        back_button = ttk.Button(
            self,
            text="Volver al Inicio",
            command=lambda: self.app.show_screen("home"))
        back_button.pack(pady=15)

    def _bind_mouse_wheel(self, canvas_to_bind):
        """Asocia el desplazamiento del ratón al canvas especificado."""
        self._current_canvas = canvas_to_bind # Guardar referencia al canvas activo
        self.app.bind_all("<MouseWheel>", self._on_mouse_wheel)

    def _unbind_mouse_wheel(self, event):
        """Desasocia el desplazamiento del ratón al canvas activo."""
        self.app.unbind_all("<MouseWheel>")
        self._current_canvas = None

    def _on_mouse_wheel(self, event):
        """Maneja el evento de la rueda del ratón para el scroll del canvas activo."""
        if self._current_canvas:
            self._current_canvas.yview_scroll(int(-1*(event.delta/120)), "units")


    def _load_bookings(self):
        """
        Carga las reservas del usuario y las muestra en las secciones correspondientes.
        """
        # Limpiar cualquier item existente en ambas secciones
        for widget in self.inner_objects_frame.winfo_children():
            widget.destroy()
        for widget in self.inner_scenarios_frame.winfo_children():
            widget.destroy()

        bookings = get_user_bookings() # Obtener reservas simuladas

        if not bookings:
            ttk.Label(self.inner_objects_frame, text="No tienes reservas de objetos activas.", bootstyle="secondary").pack(pady=20)
            ttk.Label(self.inner_scenarios_frame, text="No tienes reservas de escenarios activas.", bootstyle="secondary").pack(pady=20)
            self.update_idletasks() # Actualizar para que el scrollregion se ajuste si no hay items
            self.objects_canvas.configure(scrollregion=self.objects_canvas.bbox("all"))
            self.scenarios_canvas.configure(scrollregion=self.scenarios_canvas.bbox("all"))
            return

        has_objects = False
        has_scenarios = False

        for booking in bookings:
            if booking["type"] == "Objeto":
                has_objects = True
                ItemCard(
                    self.inner_objects_frame,
                    name=booking["name"],
                    description=booking["description"] + f"\nReserva del {booking['start_date']} al {booking['end_date']}",
                    status="Reservado", # O puedes adaptar el status a la fecha de reserva
                    daily_value=booking["daily_value"],
                    deposit_value=booking.get("deposit_value"),
                    image_path=booking.get("image_path")
                ).pack(fill=X, padx=5, pady=5)
            elif booking["type"] == "Escenario":
                has_scenarios = True
                ItemCard( # ItemCard también sirve para escenarios, puedes adaptar el texto/botones
                    self.inner_scenarios_frame,
                    name=booking["name"],
                    description=booking["description"] + f"\nReserva del {booking['start_date']} al {booking['end_date']}",
                    status="Reservado",
                    daily_value=booking["daily_value"],
                    deposit_value=booking.get("deposit_value"),
                    image_path=booking.get("image_path")
                ).pack(fill=X, padx=5, pady=5)

        if not has_objects:
             ttk.Label(self.inner_objects_frame, text="No tienes reservas de objetos activas.", bootstyle="secondary").pack(pady=20)
        if not has_scenarios:
             ttk.Label(self.inner_scenarios_frame, text="No tienes reservas de escenarios activas.", bootstyle="secondary").pack(pady=20)

        # Asegurarse de que el scrollregion se actualice después de añadir items
        self.update_idletasks()
        self.objects_canvas.configure(scrollregion=self.objects_canvas.bbox("all"))
        self.scenarios_canvas.configure(scrollregion=self.scenarios_canvas.bbox("all"))
