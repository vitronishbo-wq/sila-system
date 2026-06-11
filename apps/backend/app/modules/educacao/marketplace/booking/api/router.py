"""Router for Booking subdomain"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from apps.backend.app.api.deps import get_current_user, get_db
from apps.backend.app.modules.educacao.infrastructure.models.escola_model import EscolaModel
from apps.backend.app.core.rbac.territorial_access import verify_territorial_access
from .health import booking_health


router = APIRouter(
    prefix="/marketplace/booking",
    tags=["marketplace", "booking"],
)


@router.get("/health", name="booking_health")
async def health_check():
    """Health check para Booking"""
    return await booking_health()


@router.post("/reserve", name="reserve_vacancy")
async def reserve_vacancy(
    citizen_id: str,
    opportunity_id: str,
    user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Reservar vaga
    
    Args:
        citizen_id: ID do cidadão
        opportunity_id: ID da oportunidade
        
    Returns:
        Confirmação de reserva
    """
    # Attempt to resolve opportunity -> institution to check territorial access.
    escola_model = None
    try:
        inst_id = uuid.UUID(opportunity_id)
        escola_model = await session.get(EscolaModel, inst_id)
    except Exception:
        escola_model = None
    await verify_territorial_access(user=user, resource_territory_id=getattr(escola_model, "territory_id", None), db=session)
    # TODO: Implementar lógica completa de reserva
    return {
        "booking_id": "book_123",
        "citizen_id": citizen_id,
        "opportunity_id": opportunity_id,
        "status": "reserved",
        "expires_at": "2026-06-26T00:00:00Z",
    }


@router.get("/my-bookings/{citizen_id}", name="list_citizen_bookings")
async def list_citizen_bookings(
    citizen_id: str,
):
    """Listar reservas do cidadão
    
    Args:
        citizen_id: ID do cidadão
        
    Returns:
        Lista de reservas ativas
    """
    # TODO: Implementar lógica
    return {
        "citizen_id": citizen_id,
        "bookings": [],
        "total": 0,
    }


@router.post("/enroll", name="auto_enroll")
async def auto_enroll(
    booking_id: str,
    user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """Efetuar pré-matrícula automática
    
    Args:
        booking_id: ID da reserva
        
    Returns:
        Confirmação de matrícula
    """
    # TODO: Map booking -> institution and enforce territorial access once mapping exists
    await verify_territorial_access(user=user, resource_territory_id=None, db=session)
    return {
        "booking_id": booking_id,
        "enrollment_id": "enr_123",
        "status": "enrolled",
        "enrollment_document": "doc_url",
    }
