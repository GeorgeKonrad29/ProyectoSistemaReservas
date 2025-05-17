from fastapi import APIRouter, HTTPException
from database import get_connection
import hashlib

login_router = APIRouter()

def hash_password(password: str, salt: str) -> str:
    """Hash SHA-256 de la contraseña concatenada con el salt."""
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

def verificar_credenciales(email: str, password: str) -> bool:
    """Verifica credenciales usando hash + salt."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Contrasenia, Salt FROM Usuarios WHERE Correo = %s", (email,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_hash, salt = result
        input_hash = hash_password(password, salt)
        return input_hash == stored_hash
    return False

@login_router.post("/login")
def login(data: dict):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Campos incompletos")

    if verificar_credenciales(email, password):
        return {"message": "Login exitoso"}
    else:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
