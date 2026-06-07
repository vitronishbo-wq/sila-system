"""Health check for Ranking subdomain"""
from typing import Dict, Any


async def ranking_health() -> Dict[str, Any]:
    """Health check para serviço de Ranking
    
    Returns:
        Dict com status do serviço
    """
    return {
        "subdomain": "ranking",
        "status": "healthy",
        "description": "Ranking de instituições e programas",
        "dependencies": ["database", "cache"],
    }
