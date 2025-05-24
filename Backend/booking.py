from fastapi import APIRouter
from datetime import datetime
from database import get_connection

booking_router = APIRouter()

@booking_router.post("/create_booking")
def create_booking(data:dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reservas (Correo_Usuario, Lugar, Precio, Fecha, Hora, ID_Escenario)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data["correo"],
        data["lugar"],
        data["precio"],
        data["fecha"],
        data["hora"],
        data["id_escenario"]
    ))
    conn.commit()
    reserva_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return {"id_reserva": reserva_id}

