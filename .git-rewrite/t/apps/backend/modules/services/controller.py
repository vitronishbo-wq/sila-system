"""
Services module controller - FastAPI routes with full type safety.

This controller follows the OpenAPI contract and uses Pydantic schemas for validation.
All endpoints are properly typed with response_model for automatic Swagger documentation.
"""

from datetime import datetime

from fastapi import APIRouter

# Import API response schemas
from modules.common.schemas.api_responses import PingResponse

# Import Services module schemas
from modules.services.schemas import ServiceItem, ServicesListResponse

# Create router
router = APIRouter()


# ============================================================================
# Services Ping
# ============================================================================


@router.get(
    "/ping",
    response_model=PingResponse,
    summary="Ping",
    description="Health check do módulo services.",
    tags=["Services"],
)
async def ping():
    """Health check do módulo services."""
    return PingResponse(message="pong", timestamp=datetime.utcnow())


# ============================================================================
# List Services
# ============================================================================


@router.get(
    "/",
    response_model=ServicesListResponse,
    summary="List Services",
    description="Lista todos os serviços disponíveis no sistema.",
    tags=["Services"],
)
async def list_services() -> ServicesListResponse:
    """
    Lista todos os serviços disponíveis no sistema.

    Returns:
        ServicesListResponse: Lista de serviços
    """
    # TODO: Implementar serviço real na Fase 4 se necessário
    # Por enquanto, retorna lista de serviços básicos do sistema
    services = [
        ServiceItem(
            name="authentication",
            status="active",
            description="Serviço de autenticação e autorização",
        ),
        ServiceItem(
            name="notifications",
            status="active",
            description="Serviço de notificações",
        ),
        ServiceItem(
            name="documents",
            status="active",
            description="Serviço de gestão de documentos",
        ),
        ServiceItem(
            name="health",
            status="active",
            description="Serviço de gestão de saúde",
        ),
        ServiceItem(
            name="citizenship",
            status="active",
            description="Serviço de cidadania",
        ),
    ]

    return ServicesListResponse(
        items=services,
        total=len(services),
    )


__all__ = ["router"]
