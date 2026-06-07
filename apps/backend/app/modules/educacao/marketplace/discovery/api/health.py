"""Health check for Discovery subdomain"""
from typing import Dict, Any


async def discovery_health() -> Dict[str, Any]:
    """Health check para serviço de Discovery
    
    Returns:
        Dict com status do serviço
    """
    return {
        "subdomain": "discovery",
        "status": "healthy",
        "description": "Descoberta de vagas e programas educacionais",
        "dependencies": ["database", "elasticsearch"],
    }
