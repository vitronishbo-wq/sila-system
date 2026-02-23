from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.core.database import get_session
from app.core.exceptions import InvalidRequestError
from .deps import get_request_service, get_request_or_404, require_request_permission
from .schemas.request_schema import (
    ServiceRequestCreate, ServiceRequestResponse, ServiceRequestDetailResponse,
    ServiceRequestListResponse, ServiceRequestStatusUpdate, ServiceRequestAssign,
    ServiceRequestSearch, ServiceRequestStatsResponse
)
from ..application.services.request_service import RequestService
from ..domain.enums import ServiceType, ServiceRequestStatus

router = APIRouter(prefix="/service-requests", tags=["Pedidos de Serviço"])


@router.post("/", response_model=ServiceRequestResponse, status_code=201)
async def create_service_request(
    request_data: ServiceRequestCreate,
    service: RequestService = Depends(get_request_service)
):
    """
    Cria um novo pedido de serviço
    """
    try:
        # For now, use a default citizen_id - integrate with IAM later
        citizen_id = UUID("00000000-0000-0000-0000-000000000001")
        created_by = UUID("00000000-0000-0000-0000-000000000001")
        
        request = await service.create_request(
            citizen_id=citizen_id,
            created_by=created_by,
            service_type=ServiceType(request_data.service_type),
            title=request_data.title,
            description=request_data.description,
            channel=request_data.channel,
            priority=request_data.priority,
            metadata=request_data.metadata,
            tags=request_data.tags
        )
        
        return request
    except Exception as e:
        raise InvalidRequestError(reason=str(e)).to_http_exception()


@router.get("/me", response_model=ServiceRequestListResponse)
async def list_my_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: RequestService = Depends(get_request_service)
):
    """
    Lista pedidos do cidadão logado
    """
    # For now, use a default citizen_id - integrate with IAM later
    citizen_id = UUID("00000000-0000-0000-0000-000000000001")
    
    requests = await service.list_citizen_requests(citizen_id, skip, limit)
    
    return {
        "total": len(requests),
        "items": requests
    }


@router.get("/assigned", response_model=ServiceRequestListResponse)
async def list_assigned_requests(
    status_filter: Optional[str] = Query(None, alias="status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: RequestService = Depends(get_request_service)
):
    """
    Lista pedidos atribuídos ao operador
    """
    # For now, use a default user_id - integrate with IAM later
    user_id = UUID("00000000-0000-0000-0000-000000000002")
    
    requests = await service.list_operator_requests(user_id, status_filter, skip, limit)
    
    return {
        "total": len(requests),
        "items": requests
    }


@router.get("/pending", response_model=ServiceRequestListResponse)
async def list_pending_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: RequestService = Depends(get_request_service)
):
    """
    Lista pedidos pendentes de atribuição
    """
    requests = await service.list_pending_requests(skip, limit)
    
    return {
        "total": len(requests),
        "items": requests
    }


@router.get("/{request_id}", response_model=ServiceRequestDetailResponse)
async def get_service_request(
    request_id: UUID,
    service: RequestService = Depends(get_request_service)
):
    """
    Obtém detalhes de um pedido
    """
    request = await service.get_request(request_id, request_id)
    
    if not request:
        from app.core.exceptions import RequestNotFoundError
        raise RequestNotFoundError(request_id).to_http_exception()
    
    return request


@router.post("/{request_id}/submit", response_model=ServiceRequestResponse)
async def submit_service_request(
    request_id: UUID,
    service: RequestService = Depends(get_request_service)
):
    """
    Submete um pedido (rascunho -> submetido)
    """
    from app.core.exceptions import UnauthorizedError, InvalidRequestError
    
    try:
        # For now, use a default user_id - integrate with IAM later
        submitted_by = UUID("00000000-0000-0000-0000-000000000001")
        
        request = await service.submit_request(request_id, submitted_by)
        return request
    except PermissionError as e:
        raise UnauthorizedError(str(e)).to_http_exception()
    except Exception as e:
        raise InvalidRequestError(reason=str(e)).to_http_exception()


@router.post("/{request_id}/assign", response_model=ServiceRequestResponse)
async def assign_service_request(
    request_id: UUID,
    assign_data: ServiceRequestAssign,
    service: RequestService = Depends(get_request_service)
):
    """
    Atribui um pedido a um operador
    """
    try:
        # For now, use a default user_id - integrate with IAM later
        assigned_by = UUID("00000000-0000-0000-0000-000000000002")
        
        request = await service.assign_request(
            request_id,
            assign_data.assigned_to_user_id,
            assigned_by
        )
        return request
    except Exception as e:
        raise InvalidRequestError(reason=str(e)).to_http_exception()


@router.patch("/{request_id}/status", response_model=ServiceRequestResponse)
async def update_service_request_status(
    request_id: UUID,
    status_data: ServiceRequestStatusUpdate,
    service: RequestService = Depends(get_request_service)
):
    """
    Atualiza status de um pedido
    """
    from app.core.exceptions import StatusTransitionError
    
    try:
        # For now, use a default user_id - integrate with IAM later
        changed_by = UUID("00000000-0000-0000-0000-000000000002")
        
        request = await service.change_status(
            request_id,
            status_data.status,
            changed_by,
            status_data.reason
        )
        return request
    except ValueError as e:
        raise InvalidRequestError(reason=str(e)).to_http_exception()


@router.post("/search", response_model=ServiceRequestListResponse)
async def search_service_requests(
    search: ServiceRequestSearch,
    service: RequestService = Depends(get_request_service)
):
    """
    Pesquisa avançada de pedidos
    """
    filters = search.model_dump(exclude={"query", "skip", "limit", "start_date", "end_date"}, exclude_none=True)
    
    requests, total = await service.search_requests(
        search.query or "",
        filters,
        search.skip,
        search.limit
    )
    
    return {
        "total": total,
        "items": requests
    }


@router.get("/stats/overview", response_model=ServiceRequestStatsResponse)
async def get_request_stats(
    service: RequestService = Depends(get_request_service)
):
    """
    Estatísticas gerais de pedidos
    """
    return await service.get_statistics()
