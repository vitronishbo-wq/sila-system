"""Router for Discovery subdomain"""
from fastapi import APIRouter

from .health import discovery_health

router = APIRouter(
    prefix="/marketplace/discovery",
    tags=["marketplace", "discovery"],
)


@router.get("/health", name="discovery_health")
async def health_check():
    """Health check para Discovery"""
    return await discovery_health()


@router.get("/opportunities", name="list_opportunities")
async def list_opportunities(
    level: str | None = None,
    institution_id: str | None = None,
    available_only: bool = True,
):
    """Listar oportunidades educacionais disponíveis
    
    Args:
        level: Nível educacional (básico, médio, superior, etc)
        institution_id: ID da instituição
        available_only: Mostrar apenas vagas disponíveis
        
    Returns:
        Lista de oportunidades
    """
    # TODO: Implementar lógica
    return {
        "opportunities": [],
        "total": 0,
        "page": 1,
    }


@router.get("/programs", name="list_programs")
async def list_programs(
    institution_id: str | None = None,
):
    """Listar programas educacionais
    
    Args:
        institution_id: ID da instituição
        
    Returns:
        Lista de programas
    """
    # TODO: Implementar lógica
    return {
        "programs": [],
        "total": 0,
    }


@router.get("/institutions", name="list_institutions")
async def list_institutions():
    """Listar instituições educacionais
    
    Returns:
        Lista de instituições
    """
    # TODO: Implementar lógica
    return {
        "institutions": [],
        "total": 0,
    }
