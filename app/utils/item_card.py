"""
utils/item_card.py: Contiene la clase para la tarjeta individual de un objeto de préstamo.
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
# from PIL import Image, ImageTk # Descomentar si necesitas cargar PNG/JPG

class ItemCard(ttk.Frame):
    """
    Representa una "tarjeta" de un objeto disponible para préstamo.
    """
    def __init__(self, parent, name, description, status, daily_value, deposit_value=None, image_path=None, **kwargs):
        super().__init__(parent, bootstyle="light", relief="raised", borderwidth=1, **kwargs)

        self.name = name
        self.description = description
        self.status = status
        self.daily_value = daily_value
        self.deposit_value = deposit_value
        self.image_path = image_path

        self._create_widgets()

    def _create_widgets(self):
        """
        Crea y organiza los widgets dentro de la tarjeta del objeto.
        """
        # --- Contenedor principal para la información del item ---
        info_frame = ttk.Frame(self)
        info_frame.pack(fill=X, padx=10, pady=10)

        # --- Imagen del Objeto (lado izquierdo) ---
        if self.image_path:
            try:
                # Para cargar PNG/JPG, necesitarías Pillow:
                # img = Image.open(self.image_path)
                # img = img.resize((100, 100), Image.Resampling.LANCZOS) # Ejemplo de redimensionamiento
                # self.tk_image = ImageTk.PhotoImage(img)

                # Si solo usas GIF o tienes la imagen en el formato correcto de tk.PhotoImage:
                self.tk_image = ttk.PhotoImage(file=self.image_path)
                image_label = ttk.Label(info_frame, image=self.tk_image, relief="solid", borderwidth=1)
                image_label.pack(side=LEFT, padx=(0, 10), pady=5)
            except Exception as e:
                print(f"Error al cargar imagen {self.image_path}: {e}")
                placeholder_label = ttk.Label(info_frame, text="[No Image]", bootstyle="danger")
                placeholder_label.pack(side=LEFT, padx=(0, 10), pady=5)
        else:
            placeholder_label = ttk.Label(info_frame, text="[No Image]", bootstyle="secondary")
            placeholder_label.pack(side=LEFT, padx=(0, 10), pady=5)


        # --- Detalles del Objeto (lado derecho) ---
        details_frame = ttk.Frame(info_frame)
        details_frame.pack(side=LEFT, fill=X, expand=True)

        # Nombre
        name_label = ttk.Label(details_frame, text=self.name, font=("Helvetica", 12, "bold"), bootstyle="primary")
        name_label.pack(anchor=W, pady=(0, 2))

        # Estado/Disponibilidad
        status_style = "success" if self.status == "Disponible" else "warning"
        status_label = ttk.Label(details_frame, text=f"Estado: {self.status}", bootstyle=status_style)
        status_label.pack(anchor=W, pady=2)

        # Descripción breve
        description_label = ttk.Label(details_frame, text=self.description, wraplength=400, justify="left", bootstyle="secondary")
        description_label.pack(anchor=W, pady=2)

        # --- Información de Valor ---
        value_frame = ttk.Frame(details_frame)
        value_frame.pack(anchor=W, pady=5)

        daily_value_label = ttk.Label(value_frame, text=f"Valor diario: ${self.daily_value:.2f}", bootstyle="info")
        daily_value_label.pack(side=LEFT, padx=(0, 10))

        if self.deposit_value is not None:
            deposit_label = ttk.Label(value_frame, text=f"Depósito: ${self.deposit_value:.2f}", bootstyle="info")
            deposit_label.pack(side=LEFT, padx=(0, 10))

        included_shipping_label = ttk.Label(value_frame, text="Envío incluido", bootstyle="success")
        included_shipping_label.pack(side=LEFT)


        # --- Botón de Acción ---
        action_button = ttk.Button(self, text="Solicitar Préstamo", bootstyle="primary")
        action_button.pack(pady=(0, 10))
        action_button.config(command=lambda: self._request_loan(self.name))

    def _request_loan(self, item_name):
        """Método de ejemplo para solicitar un préstamo."""
        print(f"Solicitando préstamo de: {item_name}")
        ttk.Messagebox.showinfo("Solicitud de Préstamo", f"Has solicitado '{item_name}'. Un administrador se pondrá en contacto.")