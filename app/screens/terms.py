import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from utils.utils import read_archive


class TermsScreen(ttk.Frame):
    def __init__(self, parent, controller, terms_filepath):
        super().__init__(parent)
        self.controller = controller
        self.terms_filepath = terms_filepath
        self.create_widgets()

    def create_widgets(self):
        term_frame = ttk.Frame(
            self,
            width=900,
            height=300
        )
        term_frame.place(
            relx=0.5,
            rely=0.5,
            anchor=CENTER
        )
        term_frame.pack_propagate(False)

        ttk.Label(
            term_frame,
            text="Terminos y Condiciones Justos",
            justify="center",
            padding=10,
            font=("Arial", 20, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky="ew") # Adjusted row and added columnspan

        self.text_widget = ttk.Text(
            # Store text_widget as an instance variable
            term_frame,
            wrap=WORD,
            font=("Arial", 12),
            spacing3=5,
            padx=10,
            pady=10
        )

        scrollbar = ttk.Scrollbar(
            term_frame,
            orient=VERTICAL,
            command=self.text_widget.yview
            # Use self.text_widget
        )
        terms = read_archive(self.terms_filepath)
        self.text_widget.configure(
            # Use self.text_widget
            yscrollcommand=scrollbar.set
        )
        self.text_widget.insert(END, terms)
        # Use self.text_widget
        self.text_widget.configure(state=DISABLED)
        # Use self.text_widget

        # Diseño con grid
        self.text_widget.grid(row=1, column=0, sticky="nsew")
        # Placed in row 1, column 0
        scrollbar.grid(row=1, column=1, sticky="ns")
        # Placed in row 1, column 1

        # Configurar expansión
        term_frame.grid_columnconfigure(0, weight=1)
        # Corrected frame to term_frame
        term_frame.grid_rowconfigure(
            1,
            weight=1
        )
        # Adjusted row to 1 for text_widget
        return_button = ttk.Button(
            term_frame,
            text="Regresar",
            command=self._return_to_login, # Call a new method for clarity
            bootstyle=PRIMARY # Use a ttkbootstrap style
        )
        return_button.grid(row=2, column=0, columnspan=2, pady=20) # Place in a new row, centered

        # Vincular eventos de scroll
        self.text_widget.bind(
            "<MouseWheel>",
            self._on_mousewheel
        )
        # Bind to self._on_mousewheel
        self.text_widget.bind(
            "<Button-4>",
            self._on_mousewheel
        )  # Linux
        self.text_widget.bind(
            "<Button-5>",
            self._on_mousewheel
        )  # Linux

    def _return_to_login(self):
        self.controller.show_screens("signup")

    # Función para desplazamiento con rueda del mouse/trackpad
    def _on_mousewheel(self, event):
        # Added self as first argument
        if event.delta:
            self.text_widget.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )
        elif event.num == 4:  # Eventos en Linux (Scroll Up)
            self.text_widget.yview_scroll(-1, "units")
        elif event.num == 5:  # Eventos en Linux (Scroll Down)
            self.text_widget.yview_scroll(1, "units")
