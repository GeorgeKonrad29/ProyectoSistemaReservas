# bookings.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class BookingsScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # configuracion inicial
        self.setup_scrollbar_area()
        self.create_inner_frame()
        self.create_catalog_items()
        self.setup_events()

    def setup_scrollbar_area(self):
        # configurar el area del canvas y el scrollbar
        self.canvas = ttk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(
            self,
            orient=VERTICAL,
            command=self.canvas.yview
        )
        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )
        # empaquetado
        self.scrollbar.pack(
            side=RIGHT,
            fill=Y
        )
        self.canvas.pack(
            side=LEFT,
            fill=BOTH,
            expand=True
        )

    def create_inner_frame(self):
        # crea el contenedor interno
        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas.create_window(
            (0, 0),
            window=self.inner_frame,
            anchor=NW,
            tags="inner_frame"
        )

    def create_catalog_items(self):
        # genera los elementos del catalogo
        for i in range(50):
            item = ttk.Frame(self.inner_frame, padding=10)
            ttk.Label(
                item,
                text=f"Producto {i + 1}",
                font=("Arial", 15)
            ).pack(side=LEFT)
            item.pack(
                fil=X,
                pady=5,
                padx=10
            )

    def setup_events(self):
         # Evento de rueda del ratón
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.inner_frame.bind("<MouseWheel>", self.on_mouse_wheel)

    def update_scrollregion(self, event):
        """Actualiza el área de desplazamiento"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_canvas_width(self, event):
        """Ajusta el ancho del frame interno al Canvas"""
        self.canvas.itemconfig("inner_frame", width=event.width)

    def on_mouse_wheel(self, event):
        """Maneja el evento de la rueda del ratón"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

