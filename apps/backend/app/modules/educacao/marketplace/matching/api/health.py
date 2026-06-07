"""Health check for Matching subdomain"""
from typing import Dict, Any


async def matching_health() -> Dict[str, Any]:
    """Health check para serviço de Matching
    
    Returns:
        Dict com status do serviço
    """
    return {
        "subdomain": "matching",
        "status": "healthy",
        "description": "Matching automático baseado em elegibilidade",
        "dependencies": ["database", "eligibility_engine"],
    }
