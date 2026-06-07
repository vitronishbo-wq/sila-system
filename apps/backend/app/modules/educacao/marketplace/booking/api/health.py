"""Health check for Booking subdomain"""
from typing import Dict, Any


async def booking_health() -> Dict[str, Any]:
    """Health check para serviço de Booking
    
    Returns:
        Dict com status do serviço
    """
    return {
        "subdomain": "booking",
        "status": "healthy",
        "description": "Reserva de vagas e pré-matrícula",
        "dependencies": ["database", "enrollment_service"],
    }
