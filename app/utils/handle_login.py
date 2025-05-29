import requests
from ttkbootstrap.dialogs import Messagebox


def handle_login(email: str, password: str):
    if not email or not password:
        Messagebox.show_error("Todos los campos son obligatorios", "Error")
        return
    try:
        response = requests.post("http://localhost:8000/login", json={
            "email": email,
            "password": password
        })
        response.raise_for_status()  # Lanza un error si la respuesta no es 200
        Messagebox.show_info("Login exitoso", "Éxito")
        return True
        # Aquí puedes redirigir a otra pantalla después de un login exitoso
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            Messagebox.show_error("Credenciales inválidas", "Error")
        elif e.response.status_code == 403:
            Messagebox.show_error("Cuenta bloqueada por 7 intentos fallidos", "Error")
        else:
            Messagebox.show_error("Error de conexión", "Error")
