import os
import stripe
import smtplib
from email.message import EmailMessage
from fastapi import APIRouter, Request, HTTPException
from database import get_connection
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_PASS = os.getenv("SMTP_PASS")

payment_router = APIRouter()

@payment_router.post("/payment")
def create_payment(data: dict):
    reserva_id = data["id_reserva"]

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT Precio FROM reservas WHERE ID_Reserva = %s", (reserva_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        raise HTTPException(404, "Reserva no encontrada")

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "mxn",
                "product_data": {"name": f"Reserva {reserva_id}"},
                "unit_amount": int(row["Precio"] * 100),
            },
            "quantity": 1,
        }],
        metadata={"reserva_id": str(reserva_id)},
        mode="payment",
        success_url="http://localhost:8000/exito",
        cancel_url="http://localhost:8000/cancelado"
    )

    return {"url": session.url}

@payment_router.post("/stripe/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except stripe.error.SignatureVerificationError:
        raise HTTPException(400, "Webhook inválido")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        reserva_id = session["metadata"].get("reserva_id")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Confirmar la reserva
        cursor.execute("UPDATE reservas SET Estado = 'confirmada' WHERE ID_Reserva = %s", (reserva_id,))
        conn.commit()

        # Obtener datos para el correo
        cursor.execute("""
            SELECT r.ID_Reserva, r.Correo_Usuario, r.Lugar, r.Precio, r.Fecha, r.ID_Escenario, e.Direccion
            FROM reservas r
            JOIN escenario e ON r.ID_Escenario = e.ID_Escenario
            WHERE r.ID_Reserva = %s
        """, (reserva_id,))
        reserva_info = cursor.fetchone()

        cursor.close()
        conn.close()

        if reserva_info:
            enviar_correo_confirmacion(reserva_info)

    return {"status": "ok"}

def enviar_correo_confirmacion(reserva_info):
    correo_usuario = reserva_info["Correo_Usuario"]

    mensaje = EmailMessage()
    mensaje["From"] = SMTP_USER
    mensaje["To"] = correo_usuario
    mensaje["Subject"] = f"Confirmación de Pago - Reserva #{reserva_info['ID_Reserva']}"

    cuerpo = f"""Hola,

Tu pago ha sido recibido exitosamente.

Detalles de la reserva:
- Lugar: {reserva_info['Lugar']}
- Dirección: {reserva_info['Direccion']}
- Fecha: {reserva_info['Fecha']}
- Precio: ${reserva_info['Precio']}
- ID Escenario: {reserva_info['ID_Escenario']}

Gracias por usar nuestro servicio.
"""

    mensaje.set_content(cuerpo)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(mensaje)
            print("Correo enviado con éxito")
    except Exception as e:
        print("Error al enviar el correo:", str(e))
