import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv() 

def get_connection():
    return mysql.connector.connect (
        host=os.getenv("192.168.0.11"),
        user=os.getenv("Admin"),
        password=os.getenv("Jorgeluis9"),
        database=os.getenv("ProyectoReservas")
    )
