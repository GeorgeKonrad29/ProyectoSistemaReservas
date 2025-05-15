# bookings.py
import ttkbootstrap as ttk

class BookingsScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
    
    def create_widgets(self):
        # Contenido de la pantalla
        pass