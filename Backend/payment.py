import os
import stripe
from fastapi import APIRouter, Request, HTTPException
from database import get_connection
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

payment_router = APIRouter(tags=["pagos"])

@payment_router.post("/payment")
def create_payment(data: dict):
    """
    Genera una sesión de Stripe Checkout para la reserva indicada.
    """
    reserva_id = data.get("id_reserva")
    if not reserva_id:
        raise HTTPException(400, "Falta id_reserva en el payload")

    # Tomamos el precio real desde la BD
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
        cancel_url="http://localhost:8000/cancelado",
    )
    return {"url": session.url}


@payment_router.post("/stripe/webhook")
async def stripe_webhook(request: Request):
    """
    Recibe notificaciones de Stripe y marca la reserva como 'confirmada'.
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, secret)
    except stripe.error.SignatureVerificationError:
        raise HTTPException(400, "Webhook inválido")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        reserva_id = session["metadata"].get("reserva_id")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE reservas SET Estado = 'confirmada' WHERE ID_Reserva = %s",
            (reserva_id,)
        )
        conn.commit()
        cur.close()
        conn.close()

    return {"status": "ok"}
