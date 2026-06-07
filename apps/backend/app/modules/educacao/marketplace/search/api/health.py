"""Health check for Search subdomain"""
from typing import Dict, Any


async def search_health() -> Dict[str, Any]:
    """Health check para serviço de Search
    
    Returns:
        Dict com status do serviço
    """
    return {
        "subdomain": "search",
        "status": "healthy",
        "description": "Busca avançada com filtros complexos",
        "dependencies": ["database", "search_engine", "geolocation_service"],
    }
