# utils/mouse_events.py

def bind_mousewheel(widget, scroll_target=None):
    """
    Vincula eventos del mouse para permitir scroll en widgets de ttkbootstrap o tkinter.
    
    :param widget: Widget que recibe el evento del mouse (por ejemplo, Text).
    :param scroll_target: Widget que debe desplazarse. Si no se especifica, se usa el mismo.
    """
    if scroll_target is None:
        scroll_target = widget

    def _on_mousewheel(event):
        # Soporte para Windows/macOS
        if hasattr(event, "delta") and event.delta:
            scroll_target.yview_scroll(int(-1 * (event.delta / 120)), "units")
        # Soporte para Linux (Button-4 / Button-5)
        elif event.num == 4:
            scroll_target.yview_scroll(-1, "units")
        elif event.num == 5:
            scroll_target.yview_scroll(1, "units")

    # Vincular eventos compatibles
    widget.bind("<MouseWheel>", _on_mousewheel)   # Windows y macOS
    widget.bind("<Button-4>", _on_mousewheel)      # Linux (scroll up)
    widget.bind("<Button-5>", _on_mousewheel)      # Linux (scroll down)
