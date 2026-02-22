# modules/citizenship/endpoints.py
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.session import get_async_db as get_db
from core.security import get_current_active_user
from modules.citizenship.models.citizen import Citizen
from modules.citizenship.schemas.citizenship import (
    CitizenshipServiceRead,
    ServiceRequestCreate,
    ServiceRequestRead,
    ServiceStatus,
)
from modules.citizenship.services.citizenship_service import CitizenshipService

router = APIRouter(prefix="/citizenship", tags=["citizenship"])


@router.get("/ping")
async def ping() -> dict:
    """Health check do módulo citizenship."""
    return {
        "status": "healthy",
        "module": "citizenship",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "services": [
            "service_catalog",
            "request_management",
            "status_tracking",
            "notification_system",
        ],
    }


@router.get("/services", response_model=List[CitizenshipServiceRead])
async def get_available_services(
    category: Optional[str] = Query(None, description="Filtrar por categoria"),
    db: AsyncSession = Depends(get_db),
):
    """Lista serviços disponíveis, opcionalmente filtrados por categoria."""
    services = await CitizenshipService.get_available_services(db, category)
    return services


@router.post("/requests", response_model=ServiceRequestRead, status_code=status.HTTP_201_CREATED)
async def create_service_request(
    request_data: ServiceRequestCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """Cria nova solicitação de serviço para o usuário autenticado."""
    request = await CitizenshipService.create_request(
        db=db, citizen_id=current_user.id, request_data=request_data
    )
    return request


@router.get("/requests/user", response_model=List[ServiceRequestRead])
async def get_user_requests(
    status_filter: Optional[ServiceStatus] = Query(None, description="Filtrar por status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """Lista solicitações do usuário autenticado com paginação e filtro opcional."""
    requests = await CitizenshipService.get_user_requests(
        db=db,
        citizen_id=current_user.id,
        status_filter=status_filter,
        skip=skip,
        limit=limit,
    )
    return requests


@router.get("/requests/{request_id}", response_model=ServiceRequestRead)
async def get_request_details(
    request_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """Retorna detalhes completos de uma solicitação do usuário."""
    request = await CitizenshipService.get_request_by_id(
        db=db, request_id=request_id, citizen_id=current_user.id
    )
    if not request:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")
    return request


@router.patch("/requests/{request_id}/cancel", response_model=ServiceRequestRead)
async def cancel_request(
    request_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """Cancela solicitação do usuário, se permitido."""
    cancelled = await CitizenshipService.cancel_request(
        db=db, request_id=request_id, citizen_id=current_user.id
    )
    if not cancelled:
        raise HTTPException(
            status_code=404,
            detail="Solicitação não encontrada ou não pode ser cancelada",
        )
    return cancelled


@router.get("/requests/{request_id}/status")
async def get_request_status(
    request_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """Retorna status atual de uma solicitação do usuário."""
    status_info = await CitizenshipService.get_request_status(
        db=db, request_id=request_id, citizen_id=current_user.id
    )
    if not status_info:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")
    return status_info