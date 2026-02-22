"""
Endpoints principais do módulo Citizenship.

Este módulo implementa os endpoints essenciais para:
- Health check e diagnóstico
- Catálogo de serviços disponíveis
- Gestão de solicitações de cidadania
- Controle de status e acompanhamento
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.session import get_async_db as get_db
from modules.auth.auth_utils import get_current_active_user

from .models.citizen import Citizen
from .schemas.citizenship import (
    CitizenshipServiceRead,
    ServiceRequestCreate,
    ServiceRequestRead,
    ServiceStatus,
)
from .services.citizenship_service import CitizenshipService

router = APIRouter()


@router.get("/ping")
async def ping():
    """
    Health check do módulo Citizenship.

    Verifica se o módulo está operacional e retorna informações básicas.
    """
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
    category: Optional[str] = Query(
        None, description="Filtrar por categoria de serviço"
    ),
    db: AsyncSession = Depends(get_db),
):
    """
    Lista de serviços disponíveis no catálogo de cidadania.

    Retorna todos os serviços disponíveis ou filtra por categoria.
    """
    try:
        services = await CitizenshipService.get_available_services(db, category)
        return services
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar serviços: {str(e)}",
        )


@router.post(
    "/requests", response_model=ServiceRequestRead, status_code=status.HTTP_201_CREATED
)
async def create_service_request(
    request_data: ServiceRequestCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Criar nova solicitação de serviço de cidadania.

    Permite ao usuário autenticado criar uma nova solicitação de serviço.
    """
    try:
        service_request = await CitizenshipService.create_request(
            db=db, citizen_id=current_user.id, request_data=request_data
        )
        return service_request
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar solicitação: {str(e)}",
        )


@router.get("/requests/user", response_model=List[ServiceRequestRead])
async def get_user_requests(
    status_filter: Optional[ServiceStatus] = Query(
        None, description="Filtrar por status"
    ),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Lista solicitações do usuário autenticado.

    Retorna todas as solicitações do usuário com opção de filtro por status.
    """
    try:
        requests = await CitizenshipService.get_user_requests(
            db=db,
            citizen_id=current_user.id,
            status_filter=status_filter,
            skip=skip,
            limit=limit,
        )
        return requests
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar solicitações: {str(e)}",
        )


@router.get("/requests/{request_id}", response_model=ServiceRequestRead)
async def get_request_details(
    request_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Detalhes completos de uma solicitação específica.

    Retorna informações detalhadas da solicitação incluindo status e histórico.
    """
    try:
        request = await CitizenshipService.get_request_by_id(
            db=db, request_id=request_id, citizen_id=current_user.id
        )
        if not request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Solicitação não encontrada",
            )
        return request
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar solicitação: {str(e)}",
        )


@router.patch("/requests/{request_id}/cancel", response_model=ServiceRequestRead)
async def cancel_request(
    request_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Cancelar uma solicitação de serviço.

    Permite ao usuário cancelar uma solicitação que ainda pode ser cancelada.
    """
    try:
        cancelled_request = await CitizenshipService.cancel_request(
            db=db, request_id=request_id, citizen_id=current_user.id
        )
        if not cancelled_request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Solicitação não encontrada ou não pode ser cancelada",
            )
        return cancelled_request
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao cancelar solicitação: {str(e)}",
        )


@router.get("/requests/{request_id}/status")
async def get_request_status(
    request_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Citizen = Depends(get_current_active_user),
):
    """
    Status atual de uma solicitação.

    Retorna apenas o status e informações básicas da solicitação.
    """
    try:
        status_info = await CitizenshipService.get_request_status(
            db=db, request_id=request_id, citizen_id=current_user.id
        )
        if not status_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Solicitação não encontrada",
            )
        return status_info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar status: {str(e)}",
        )
