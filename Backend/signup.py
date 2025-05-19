from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from database import get_connection
import hashlib
import os

signup_router = APIRouter()

class SignupRequest(BaseModel):
    fullname: str
    email: EmailStr
    password: str

def hash_password(password: str, salt: str) -> str:
    """Hash SHA-256 de la contraseña concatenada con el salt."""
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

@signup_router.post("/signup")
def signup(user: SignupRequest):
    conn = get_connection()
    cursor = conn.cursor()

    # Verificar si el correo ya existe
    cursor.execute("SELECT Correo FROM Usuarios WHERE Correo = %s", (user.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    # Generar salt y contraseña hasheada
    salt = os.urandom(16).hex()
    hashed_password = hash_password(user.password, salt)

    # Separar nombres y apellidos
    nombres = user.fullname.split()[0]
    apellidos = " ".join(user.fullname.split()[1:])

    # Insertar en la base de datos
    cursor.execute("""
        INSERT INTO Usuarios (Correo, Nombres, Apellidos, Contrasenia, Salt)
        VALUES (%s, %s, %s, %s, %s)
    """, (user.email, nombres, apellidos, hashed_password, salt))

    conn.commit()
    conn.close()
    return {"mensaje": "Usuario registrado exitosamente"}
