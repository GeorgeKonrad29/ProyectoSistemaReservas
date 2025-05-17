from fastapi import FastAPI
from login import login_router
from signup import signup_router

app = FastAPI()

# Incluir routers
app.include_router(login_router)
app.include_router(signup_router)
