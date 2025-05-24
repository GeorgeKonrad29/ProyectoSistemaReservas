from fastapi import FastAPI
from login import login_router
from signup import signup_router
from booking import booking_router
from payment import payment_router


app = FastAPI()

# Incluir routers
app.include_router(login_router)
app.include_router(signup_router)
app.include_router(booking_router, prefix="/api/reservas", tags=["Reservas"])
# ← prefijo ajustado:
app.include_router(payment_router, prefix="/api/pagos",   tags=["Pagos"])

