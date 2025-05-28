from fastapi import FastAPI
from login import login_router
from signup import signup_router
from booking import booking_router
from payment import payment_router
from fastapi.responses import HTMLResponse


app = FastAPI()



@app.get("/exito", response_class=HTMLResponse)
def pago_exitoso():
    return """
    <h1>¡Pago exitoso!</h1>
    <p>Gracias por tu pago. En breve recibirás un correo de confirmación.</p>
    """

# Incluir routers
app.include_router(login_router)
app.include_router(signup_router)
app.include_router(booking_router, prefix="/api/reservas", tags=["Reservas"])
# ← prefijo ajustado:
app.include_router(payment_router, prefix="/api/pagos",   tags=["Pagos"])



