from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr  # Añadido BaseModel y EmailStr
from database import get_connection
import bcrypt
from datetime import datetime

login_router = APIRouter()

class LoginRequest(BaseModel):
    correo: EmailStr 
    contrasenia: str

def get_user_state(email: str) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT Bloqueado FROM Usuarios WHERE Correo = %s", 
                (email,)
            )
            return (result[0] if (result := cursor.fetchone()) else False)

def get_failed_attempts(email: str) -> int:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT Intentos_login FROM Usuarios WHERE Correo = %s", 
                (email,)
            )
            return (result[0] if (result := cursor.fetchone()) else 0)

def validate_credentials(email: str, password: str) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT Contrasenia FROM Usuarios WHERE Correo = %s",
                (email,)
            )
            result = cursor.fetchone()
    
    if not result or not result[0]:
        return False
    
    stored_hash = result[0]
    return bcrypt.checkpw(password.encode(), stored_hash.encode())

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

def block_user_account(email: str):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE Usuarios SET Bloqueado = TRUE WHERE Correo = %s",
                (email,)
            )
            conn.commit()
            
@login_router.post("/login")
def login(credentials: LoginRequest):
    email = credentials.correo  # Corregido
    password = credentials.contrasenia  # Corregido

    if get_user_state(email):
        raise HTTPException(status_code=403, detail="Cuenta bloqueada")
    
    if not validate_credentials(email, password):
        attempts = get_failed_attempts(email) + 1
        update_failed_attempts(email, attempts)
        
        if attempts >= 7:
            block_user_account(email)
            raise HTTPException(
                status_code=403, 
                detail="Cuenta bloqueada por 7 intentos fallidos"
            )
        
        raise HTTPException(
            status_code=401, 
            detail=f"Credenciales inválidas. Intentos restantes: {7 - attempts}"
        )
    
    update_failed_attempts(email, 0)
    update_last_login(email)
    return {"mensaje": "Login exitoso"}