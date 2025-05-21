from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from database import get_connection
import bcrypt  

signup_router = APIRouter()

class SignupRequest(BaseModel):
    fullname: str
    email: EmailStr
    password: str

@signup_router.post("/signup")
def signup(user: SignupRequest):
    conn = get_connection()
    cursor = conn.cursor()

    # Verificar si el correo ya existe
    cursor.execute("SELECT Correo FROM Usuarios WHERE Correo = %s", (user.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    # Generar hash bcrypt 
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode()

    # Separar nombres y apellidos
    nombres = user.fullname.split()[0]
    apellidos = " ".join(user.fullname.split()[1:])

    # Insertar en la base de datos
    cursor.execute("""
        INSERT INTO Usuarios (Correo, Nombres, Apellidos, Contrasenia)
        VALUES (%s, %s, %s, %s)
    """, (user.email, nombres, apellidos, hashed_password))
    
    conn.commit()
    conn.close()
    return {"mensaje": "Usuario registrado exitosamente"}
