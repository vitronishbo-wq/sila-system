"""Integration Gateway for SILA System"""

from typing import Any, Dict

from fastapi import HTTPException

from config import settings

from .adapters.bna_adapter import BNAAdapter


class IntegrationGateway:
    """Main integration gateway for SILA system"""

    def __init__(self):
        self.adapters = {
            "bna": BNAAdapter(
                api_key=settings.BNA_API_KEY, base_url=settings.BNA_API_URL
            )
        }

    async def process_request(
        self, service: str, action: str, payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process integration request through the appropriate adapter"""
        if service not in self.adapters:
            raise HTTPException(
                status_code=400, detail=f"Unsupported integration service: {service}"
            )

        adapter = self.adapters[service]

        try:
            if not hasattr(adapter, action):
                raise HTTPException(
                    status_code=400,
                    detail=f"Action '{action}' not supported by {service} adapter",
                )

            method = getattr(adapter, action)
            return await method(**payload)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing {service} integration: {str(e)}",
            )


# Singleton instance
integration_gateway = IntegrationGateway()


# ========================================
# SCHEMAS CONSOLIDADOS
# ========================================

from pydantic import BaseModel


class EventCreate(BaseModel):
    """Schema para criação de eventos de integração"""


class EventFilter(BaseModel):
    """Schema para filtros de eventos"""


class EventResponse(BaseModel):
    """Schema para resposta de eventos"""


# ========================================
# ROTAS CONSOLIDADAS
# ========================================

from fastapi import APIRouter

# Router principal consolidado
router = APIRouter(tags=["Integration"])


# Health check endpoint
@router.get("/ping")
async def ping():
    """Health check para o módulo integration"""
    return {"status": "ok", "module": "integration"}
