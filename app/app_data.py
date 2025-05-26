"""
app_data.py: Simula una fuente de datos para los objetos de préstamo.
En una aplicación real, esto sería una base de datos, una API, etc.
"""

def get_sample_items():
    """
    Retorna una lista de objetos de ejemplo para la aplicación.
    """
    return [
        {
            "name": "Taladro Inalámbrico Bosch",
            "description": "Potente taladro de impacto con batería de larga duración, ideal para trabajos domésticos.",
            "status": "Disponible",
            "daily_value": 15000.00,
            "deposit_value": 50000.00,
            # "image_path": "assets/taladro.png" # Si tienes imágenes, usa esta ruta
        },
        {
            "name": "Libro: Cien Años de Soledad",
            "description": "Edición de bolsillo de la obra maestra de Gabriel García Márquez.",
            "status": "Disponible",
            "daily_value": 2000.00,
            "deposit_value": None,
            # "image_path": "assets/libro.png"
        },
        {
            "name": "Proyector Portátil Epson",
            "description": "Proyector compacto con resolución HD, perfecto para presentaciones o noches de cine.",
            "status": "Prestado hasta 28/05/2025",
            "daily_value": 25000.00,
            "deposit_value": 100000.00,
            # "image_path": "assets/proyector.png"
        },
        {
            "name": "Tienda de Campaña para 4 Personas",
            "description": "Tienda impermeable y fácil de montar, ideal para excursiones y camping.",
            "status": "Disponible",
            "daily_value": 18000.00,
            "deposit_value": 70000.00,
            # "image_path": "assets/tienda.png"
        },
        {
            "name": "Consola de Videojuegos Retro",
            "description": "Consola con más de 1000 juegos clásicos preinstalados. ¡Diversión garantizada!",
            "status": "Disponible",
            "daily_value": 10000.00,
            "deposit_value": 30000.00,
            # "image_path": "assets/consola.png"
        },
    ]

def get_user_bookings():
    """
    Retorna una lista de reservas de ejemplo para el usuario actual.
    """
    return [
        {
            "name": "Proyector Portátil Epson",
            "description": "Tu reserva para el proyector.",
            "daily_value": 25000.00,
            "deposit_value": 100000.00,
            "type": "Objeto",
            "start_date": "2025-06-01",
            "end_date": "2025-06-03",
            # "image_path": "assets/proyector.png"
        },
        {
            "name": "Tienda de Campaña para 4 Personas",
            "description": "Tu reserva para la tienda.",
            "daily_value": 18000.00,
            "deposit_value": 70000.00,
            "type": "Objeto",
            "start_date": "2025-07-10",
            "end_date": "2025-07-15",
            # "image_path": "assets/tienda.png"
        },
        {
            "name": "Estudio de Grabación Profesional",
            "description": "Tu reserva para el estudio.",
            "daily_value": 300000.00,
            "deposit_value": 150000.00,
            "type": "Escenario",
            "start_date": "2025-06-20",
            "end_date": "2025-06-22",
            # "image_path": "assets/estudio.png"
        },
        # Puedes añadir más reservas aquí
    ]
