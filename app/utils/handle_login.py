import requests
from ttkbootstrap.dialogs import Messagebox


def handle_login(email: str, password: str):
    if not email or not password:
        Messagebox.show_error("Todos los campos son obligatorios", "Error")
        return
    try:
        # ✅ JSON correcto con claves esperadas por el backend
        login_data = {
            "username": email,
            "password": password
        }

        response = requests.post(
            "http://localhost:8000/login",
            data=login_data,  # ✅ Cambiado de data= a json=
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        response.raise_for_status()

        login_response_data = response.json()

        Messagebox.show_info("Login exitoso", "Éxito")
        print(f"Respuesta: {login_response_data}")

        # Guardar el token en la sesión del controlador

        response.raise_for_status()  # Lanza un error si la respuesta no es 200
        Messagebox.show_info("Login exitoso", "Éxito")
        return login_response_data.get("access_token")  # Retorna el token de acceso
        # Aquí puedes redirigir a otra pantalla después de un login exitoso
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            Messagebox.show_error("Credenciales inválidas", "Error")
        elif e.response.status_code == 403:
            Messagebox.show_error("Cuenta bloqueada por 7 intentos fallidos", "Error")
        else:
            Messagebox.show_error("Error de conexión", "Error")
