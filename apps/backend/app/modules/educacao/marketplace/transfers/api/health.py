"""Health check for Transfers subdomain"""
from typing import Dict, Any


async def transfers_health() -> Dict[str, Any]:
    """Health check para serviço de Transfers
    
    Returns:
        Dict com status do serviço
    """
    return {
        "subdomain": "transfers",
        "status": "healthy",
        "description": "Transferências self-service",
        "dependencies": ["database", "curriculum_validator"],
    }
