"""Router for Transfers subdomain"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from apps.backend.app.api.deps import get_current_user, get_db
from apps.backend.app.modules.educacao.infrastructure.models.escola_model import EscolaModel
from apps.backend.app.core.rbac.territorial_access import verify_territorial_access
from .health import transfers_health


router = APIRouter(
    prefix="/marketplace/transfers",
    tags=["marketplace", "transfers"],
)


@router.get("/health", name="transfers_health")
async def health_check():
    """Health check para Transfers"""
    return await transfers_health()


@router.post("/request", name="request_transfer")
async def request_transfer(
    citizen_id: str,
    source_institution_id: str,
    destination_institution_id: str,
    source_program_id: str,
    destination_program_id: str,
    user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Solicitar transferência self-service
    
    Args:
        citizen_id: ID do cidadão
        source_institution_id: Instituição de origem
        destination_institution_id: Instituição de destino
        source_program_id: Programa de origem
        destination_program_id: Programa de destino
        
    Returns:
        Confirmação de solicitação
    """
    # Territorial checks: ensure user can access both source and destination institutions
    src_escola = None
    dst_escola = None
    try:
        src_id = uuid.UUID(source_institution_id)
        src_escola = await session.get(EscolaModel, src_id)
    except Exception:
        src_escola = None
    try:
        dst_id = uuid.UUID(destination_institution_id)
        dst_escola = await session.get(EscolaModel, dst_id)
    except Exception:
        dst_escola = None
    # Verify access for source and destination; missing mapping -> best-effort
    await verify_territorial_access(user=user, resource_territory_id=getattr(src_escola, "territory_id", None), db=session)
    await verify_territorial_access(user=user, resource_territory_id=getattr(dst_escola, "territory_id", None), db=session)

    return {
        "transfer_id": "trans_123",
        "citizen_id": citizen_id,
        "status": "pending_validation",
        "created_at": "2026-05-26T00:00:00Z",
    }


@router.get("/my-transfers/{citizen_id}", name="list_citizen_transfers")
async def list_citizen_transfers(
    citizen_id: str,
):
    """Listar histórico de transferências
    
    Args:
        citizen_id: ID do cidadão
        
    Returns:
        Histórico de transferências
    """
    # TODO: Implementar lógica
    return {
        "citizen_id": citizen_id,
        "transfers": [],
        "total": 0,
    }


@router.get("/compatibility", name="check_compatibility")
async def check_compatibility(
    source_program_id: str,
    destination_program_id: str,
):
    """Verificar compatibilidade curricular entre programas
    
    Args:
        source_program_id: ID do programa de origem
        destination_program_id: ID do programa de destino
        
    Returns:
        Análise de compatibilidade
    """
    # TODO: Implementar lógica
    return {
        "source_program_id": source_program_id,
        "destination_program_id": destination_program_id,
        "compatible": True,
        "credits_transferred": 0,
        "additional_requirements": [],
    }
