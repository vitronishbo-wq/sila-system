"""Health check for Admissions subdomain"""
from typing import Dict, Any


async def admissions_health() -> Dict[str, Any]:
    """Health check para serviço de Admissions
    
    Returns:
        Dict com status do serviço
    """
    return {
        "subdomain": "admissions",
        "status": "healthy",
        "description": "Admissão automática e validação",
        "dependencies": ["database", "document_verification", "eligibility_validator"],
    }
