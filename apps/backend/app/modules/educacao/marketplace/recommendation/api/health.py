"""Health check for Recommendation subdomain"""
from typing import Dict, Any


async def recommendation_health() -> Dict[str, Any]:
    """Health check para serviço de Recommendation
    
    Returns:
        Dict com status do serviço
    """
    return {
        "subdomain": "recommendation",
        "status": "healthy",
        "description": "Recomendações personalizadas via ML",
        "dependencies": ["database", "ml_model", "cache"],
    }
