from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.modules.governance.statistics.api.deps import get_dashboard_service
from app.modules.governance.statistics.api.schemas.dashboard_schema import DashboardCreate, DashboardListaResponse, DashboardResponse, DashboardUpdate
from app.modules.governance.statistics.application.services.dashboard_service import DashboardService
from app.modules.governance.statistics.exceptions import EstatisticaNotFoundError
router = APIRouter(prefix='/dashboards', tags=['Estatistica - Dashboards'])

@router.post('/', response_model=DashboardResponse, status_code=status.HTTP_201_CREATED)
async def criar_dashboard(data: DashboardCreate, service: DashboardService=Depends(get_dashboard_service)) -> DashboardResponse:
    return DashboardResponse.model_validate(await service.criar_dashboard(data.model_dump()))

@router.get('/', response_model=DashboardListaResponse)
async def listar_dashboards(pagina: int=Query(1, ge=1), tamanho_pagina: int=Query(20, ge=1, le=100), service: DashboardService=Depends(get_dashboard_service)) -> DashboardListaResponse:
    offset = (pagina - 1) * tamanho_pagina
    dashboards = await service.listar_dashboards(limit=tamanho_pagina, offset=offset)
    return DashboardListaResponse(dashboards=[DashboardResponse.model_validate(d) for d in dashboards], total=len(dashboards))

@router.get('/{dashboard_id}', response_model=DashboardResponse)
async def obter_dashboard(dashboard_id: int, service: DashboardService=Depends(get_dashboard_service)) -> DashboardResponse:
    try:
        return DashboardResponse.model_validate(await service.obter_dashboard(dashboard_id))
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.patch('/{dashboard_id}', response_model=DashboardResponse)
async def atualizar_dashboard(dashboard_id: int, data: DashboardUpdate, service: DashboardService=Depends(get_dashboard_service)) -> DashboardResponse:
    try:
        dashboard = await service.atualizar_dashboard(dashboard_id, data.model_dump(exclude_unset=True))
        return DashboardResponse.model_validate(dashboard)
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{dashboard_id}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_dashboard(dashboard_id: int, service: DashboardService=Depends(get_dashboard_service)) -> None:
    try:
        await service.deletar_dashboard(dashboard_id)
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))