"""Router for Admissions subdomain"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from apps.backend.app.api.deps import get_current_user, get_db
from apps.backend.app.modules.educacao.infrastructure.models.escola_model import EscolaModel
from apps.backend.app.core.rbac.territorial_access import verify_territorial_access
from .health import admissions_health


router = APIRouter(
    prefix="/marketplace/admissions",
    tags=["marketplace", "admissions"],
)


@router.get("/health", name="admissions_health")
async def health_check():
    """Health check para Admissions"""
    return await admissions_health()


@router.post("/process", name="process_admission")
async def process_admission(
    citizen_id: str,
    opportunity_id: str,
    user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Processar admissão automática
    
    Args:
        citizen_id: ID do cidadão
        opportunity_id: ID da oportunidade
        
    Returns:
        Resultado do processamento
    """
    # Attempt to resolve opportunity -> institution to check territorial access.
    escola_model = None
    try:
        inst_id = uuid.UUID(opportunity_id)
        escola_model = await session.get(EscolaModel, inst_id)
    except Exception:
        escola_model = None
    await verify_territorial_access(user=user, resource_territory_id=getattr(escola_model, "territory_id", None), db=session)
    # TODO: Implementar lógica
    return {
        "admission_id": "adm_123",
        "citizen_id": citizen_id,
        "opportunity_id": opportunity_id,
        "status": "approved",
        "decision_at": "2026-05-26T00:00:00Z",
    }


@router.get("/status/{admission_id}", name="get_admission_status")
async def get_admission_status(
    admission_id: str,
):
    """Verificar status de admissão
    
    Args:
        admission_id: ID da admissão
        
    Returns:
        Status detalhado
    """
    # TODO: Implementar lógica
    return {
        "admission_id": admission_id,
        "status": "approved",
        "pending_documents": [],
        "decision_letter_url": "url",
    }


@router.post("/validate", name="validate_eligibility")
async def validate_eligibility(
    citizen_id: str,
    opportunity_id: str,
    user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Validar elegibilidade
    
    Args:
        citizen_id: ID do cidadão
        opportunity_id: ID da oportunidade
        
    Returns:
        Resultado de validação
    """
    escola_model = None
    try:
        inst_id = uuid.UUID(opportunity_id)
        escola_model = await session.get(EscolaModel, inst_id)
    except Exception:
        escola_model = None
    await verify_territorial_access(user=user, resource_territory_id=getattr(escola_model, "territory_id", None), db=session)
    return {
        "citizen_id": citizen_id,
        "opportunity_id": opportunity_id,
        "eligible": True,
        "validation_errors": [],
        "required_documents": [],
    }
