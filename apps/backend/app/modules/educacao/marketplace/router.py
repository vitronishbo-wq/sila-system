"""Main router for Marketplace module"""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, status

from apps.backend.app.api.deps import get_current_user
from apps.backend.app.modules.educacao.api.deps import get_transfer_transaction_service
from apps.backend.app.modules.educacao.api.schemas.transferencia_schema import (
    TransferTransactionCreate,
    TransferTransactionResponse,
)
from apps.backend.app.modules.educacao.application.transfer_transaction_service import (
    TransferTransactionService,
)
from apps.backend.app.modules.educacao.exceptions import (
    EscolaNotFoundError,
    InvalidMatriculaStateError,
    TurmaSemVagasError,
)
from foundation.resilience import DuplicateRequestError, IdempotencyKeyMissingError

from .discovery.api.router import router as discovery_router
from .ranking.api.router import router as ranking_router
from .matching.api.router import router as matching_router
from .recommendation.api.router import router as recommendation_router
from .search.api.router import router as search_router
from .booking.api.router import router as booking_router
from .transfers.api.router import router as transfers_router
from .admissions.api.router import router as admissions_router

# Aggregated router for marketplace
router = APIRouter(
    prefix="/marketplace",
    tags=["marketplace"],
)


def _actor_id(user: dict) -> UUID:
    user_id = user.get("user_id") if user else None
    if not user_id:
        return UUID(int=0)
    return UUID(user_id)


@router.post(
    "/instant-transfer",
    response_model=TransferTransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def instant_transfer(
    data: TransferTransactionCreate,
    service: TransferTransactionService = Depends(get_transfer_transaction_service),
    user: dict = Depends(get_current_user),
    idempotency_key: str | None = Header(None, alias="Idempotency-Key"),
):
    """Executa transferência instantânea no Marketplace Educacional."""
    try:
        return await service.execute_transfer(
            student_id=data.student_id,
            current_enrollment_id=data.current_enrollment_id,
            target_institution_id=data.target_institution_id,
            target_grade=data.target_grade,
            target_shift=data.target_shift,
            academic_year=data.academic_year,
            reason=data.reason,
            actor_id=_actor_id(user),
            idempotency_key=idempotency_key,
        )
    except EscolaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except TurmaSemVagasError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except IdempotencyKeyMissingError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except DuplicateRequestError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except (InvalidMatriculaStateError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


# Include all subdomain routers
router.include_router(discovery_router)
router.include_router(ranking_router)
router.include_router(matching_router)
router.include_router(recommendation_router)
router.include_router(search_router)
router.include_router(booking_router)
router.include_router(transfers_router)
router.include_router(admissions_router)


@router.get("/health", name="marketplace_health")
async def marketplace_health():
    """Health check para todo o Marketplace
    
    Returns:
        Status de saúde do marketplace e subdomínios
    """
    return {
        "module": "marketplace",
        "status": "healthy",
        "subdomains": [
            "discovery",
            "ranking",
            "matching",
            "recommendation",
            "search",
            "booking",
            "transfers",
            "admissions",
        ],
        "version": "0.1.0",
    }


@router.get("/", name="marketplace_info")
async def marketplace_info():
    """Informações gerais do Marketplace
    
    Returns:
        Descrição e endpoints do marketplace
    """
    return {
        "name": "Citizen Educational Marketplace",
        "description": "Mercado nacional de oportunidades educacionais",
        "version": "0.1.0",
        "subdomains": {
            "discovery": "Descoberta de vagas e programas",
            "ranking": "Ranking de instituições",
            "matching": "Matching automático",
            "recommendation": "Recomendações personalizadas",
            "search": "Busca avançada",
            "booking": "Reserva de vagas",
            "transfers": "Transferências self-service",
            "admissions": "Admissão automática",
        },
        "documentation": "/docs",
    }
