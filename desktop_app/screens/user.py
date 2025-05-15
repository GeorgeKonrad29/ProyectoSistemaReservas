# Ejemplo para UserScreen (user.py)
import ttkbootstrap as ttk

class UserScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
    
    def create_widgets(self):
        # Tu contenido aquí
        ttk.Label(self, text="Pantalla de Usuario").pack()
        ttk.Button(
            self,
            text="Volver al Login",
            command=lambda: self.controller.show_screen("login")
        ).pack()