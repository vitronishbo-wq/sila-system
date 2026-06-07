from __future__ import annotations

from fastapi import APIRouter, Depends

from apps.backend.app.modules.energy.api.deps import get_geracao_service
from apps.backend.app.modules.energy.api.schemas.dashboard_schema import DashboardGeracaoResponse
from apps.backend.app.modules.energy.application.services import GeracaoService

router = APIRouter(prefix="/geracao", tags=["Energia - Geracao"])

geracao_service_dep = Depends(get_geracao_service)


@router.get("/dashboard", response_model=DashboardGeracaoResponse)
async def get_dashboard_energia(service: GeracaoService = geracao_service_dep):
    return await service.get_visao_consolidada()