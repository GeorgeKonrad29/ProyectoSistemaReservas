from fastapi import APIRouter
from datetime import datetime
from database import get_connection

booking_router = APIRouter()

@booking_router.post("/create_booking")
def create_booking(data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reservas (Correo_Usuario, Lugar, Precio, Fecha, ID_Escenario, Estado, Fecha_creacion)
        VALUES (%s, %s, %s, %s, %s, 'pendiente', %s)
    """, (
        data["correo"],
        data["lugar"],
        data["precio"],
        data["fecha"],
        data["id_escenario"],
        datetime.now()
    ))
    conn.commit()
    reserva_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return {"id_reserva": reserva_id}
