from __future__ import annotations
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.modules.governance.statistics.api.deps import get_timeseries_service
from app.modules.governance.statistics.api.schemas.timeseries_schema import TimeSeriesCreate, TimeSeriesListaResponse, TimeSeriesResponse
from app.modules.governance.statistics.application.services.timeseries_service import TimeSeriesService
from app.modules.governance.statistics.exceptions import EstatisticaNotFoundError
router = APIRouter(prefix='/timeseries', tags=['Estatistica - TimeSeries'])

@router.post('/', response_model=TimeSeriesResponse, status_code=status.HTTP_201_CREATED)
async def registrar_ponto(data: TimeSeriesCreate, service: TimeSeriesService=Depends(get_timeseries_service)) -> TimeSeriesResponse:
    try:
        return TimeSeriesResponse.model_validate(await service.registrar_ponto(data.model_dump()))
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/metrica/{metrica_id}', response_model=TimeSeriesListaResponse)
async def listar_serie(metrica_id: int, inicio: datetime | None=Query(None), fim: datetime | None=Query(None), limit: int=Query(200, ge=1, le=1000), service: TimeSeriesService=Depends(get_timeseries_service)) -> TimeSeriesListaResponse:
    try:
        pontos = await service.listar_serie(metrica_id=metrica_id, inicio=inicio, fim=fim, limit=limit)
        return TimeSeriesListaResponse(pontos=[TimeSeriesResponse.model_validate(p) for p in pontos], total=len(pontos), metrica_id=metrica_id)
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/metrica/{metrica_id}/latest', response_model=TimeSeriesResponse | None)
async def obter_ultimo(metrica_id: int, service: TimeSeriesService=Depends(get_timeseries_service)) -> TimeSeriesResponse | None:
    try:
        ponto = await service.obter_ultimo(metrica_id)
        return TimeSeriesResponse.model_validate(ponto) if ponto else None
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))