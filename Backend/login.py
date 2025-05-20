from fastapi import APIRouter, HTTPException
from database import get_connection
import hashlib
from datetime import datetime

login_router = APIRouter()

def hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((password + salt).encode()).hexdigest()

def get_state(email: str) -> bool:
    """Verifica si la cuenta está bloqueada usando context manager"""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT Bloqueado FROM Usuarios WHERE Correo = %s", 
                (email,)
            )
            result = cursor.fetchone()
            return result[0] if result else False

def get_failed_attempts(email: str) -> int:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT Intentos_login FROM Usuarios WHERE Correo = %s", 
                (email,)
            )
            result = cursor.fetchone()
            return result[0] if result else 0

def validate_credentials(email: str, password: str) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT Contrasenia, Salt FROM Usuarios WHERE Correo = %s",
                (email,)
            )
            result = cursor.fetchone()
    
    if not result:
        return False
    
    stored_hash, salt = result
    return hash_password(password, salt) == stored_hash

def update_failed_attempts(email: str, attempts: int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE Usuarios SET Intentos_login = %s WHERE Correo = %s",
                (attempts, email)
            )
            conn.commit()

def update_last_login(email: str):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE Usuarios SET Ultimo_login = %s WHERE Correo = %s",
                (datetime.now(), email)
            )
            conn.commit()

def update_blocked_status(email: str):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE Usuarios SET Bloqueado = TRUE WHERE Correo = %s",
                (email,)  # ← ¡Aquí estaba el error! La coma hace la tupla
            )
            conn.commit()

@login_router.post("/login")
def login(data: dict):
    email = data.get("email")
    password = data.get("password")

    if get_state(email):
        raise HTTPException(403, "Cuenta bloqueada")
    
    if not validate_credentials(email, password):
        attempts = get_failed_attempts(email) + 1
        update_failed_attempts(email, attempts)
        
        if attempts >= 3:
            update_blocked_status(email)
            raise HTTPException(403, "Cuenta bloqueada por 3 intentos fallidos")
        
        raise HTTPException(401, "Credenciales inválidas")
    
    update_failed_attempts(email, 0)
    update_last_login(email)
    return {"mensaje": "Login exitoso"}