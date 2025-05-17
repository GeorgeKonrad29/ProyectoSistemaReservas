from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from database import get_connection
import hashlib
import os

app = FastAPI()

# --------- MODELO DE DATOS ---------
class SignupRequest(BaseModel):
    fullname: str
    email: EmailStr
    password: str

# --------- FUNCIONES ---------
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

# --------- ENDPOINTS ---------
@app.post("/login")
def login(data: dict):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Campos incompletos")

    if verificar_credenciales(email, password):
        return {"message": "Login exitoso"}
    else:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

@app.post("/signup")
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
    apellidos = " ".join(user.fullname.split()[1:]) or "N/A"

    # Insertar en la base de datos
    cursor.execute("""
        INSERT INTO Usuarios (Correo, Nombres, Apellidos, Contrasenia, Salt)
        VALUES (%s, %s, %s, %s, %s)
    """, (user.email, nombres, apellidos, hashed_password, salt))

    conn.commit()
    conn.close()
    return {"mensaje": "Usuario registrado exitosamente"}
