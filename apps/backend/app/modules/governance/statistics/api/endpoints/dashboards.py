from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status

from apps.backend.app.modules.governance.statistics.api.deps import get_dashboard_service
from apps.backend.app.modules.governance.statistics.api.schemas.dashboard_schema import (
    DashboardCreate,
    DashboardListaResponse,
    DashboardResponse,
    DashboardUpdate,
)
from apps.backend.app.modules.governance.statistics.application.services.dashboard_service import (
    DashboardService,
)
from apps.backend.app.modules.governance.statistics.exceptions import EstatisticaNotFoundError

router = APIRouter(prefix="/dashboards", tags=["Estatistica - Dashboards"])

dashboard_service_dep = Depends(get_dashboard_service)
pagina_query = Query(1, ge=1)
tamanho_pagina_query = Query(20, ge=1, le=100)


@router.post("/", response_model=DashboardResponse, status_code=status.HTTP_201_CREATED)
async def criar_dashboard(
    data: DashboardCreate, service: DashboardService = dashboard_service_dep
) -> DashboardResponse:
    return DashboardResponse.model_validate(await service.criar_dashboard(data.model_dump()))


@router.get("/", response_model=DashboardListaResponse)
async def listar_dashboards(
    pagina: int = pagina_query,
    tamanho_pagina: int = tamanho_pagina_query,
    service: DashboardService = dashboard_service_dep,
) -> DashboardListaResponse:
    offset = (pagina - 1) * tamanho_pagina
    dashboards = await service.listar_dashboards(limit=tamanho_pagina, offset=offset)
    return DashboardListaResponse(
        dashboards=[DashboardResponse.model_validate(d) for d in dashboards], total=len(dashboards)
    )


@router.get("/{dashboard_id}", response_model=DashboardResponse)
async def obter_dashboard(
    dashboard_id: int, service: DashboardService = dashboard_service_dep
) -> DashboardResponse:
    try:
        return DashboardResponse.model_validate(await service.obter_dashboard(dashboard_id))
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{dashboard_id}", response_model=DashboardResponse)
async def atualizar_dashboard(
    dashboard_id: int,
    data: DashboardUpdate,
    service: DashboardService = dashboard_service_dep,
) -> DashboardResponse:
    try:
        dashboard = await service.atualizar_dashboard(
            dashboard_id, data.model_dump(exclude_unset=True)
        )
        return DashboardResponse.model_validate(dashboard)
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{dashboard_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_dashboard(
    dashboard_id: int, service: DashboardService = dashboard_service_dep
) -> None:
    try:
        await service.deletar_dashboard(dashboard_id)
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc