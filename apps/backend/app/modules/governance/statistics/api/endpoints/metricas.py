from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.modules.governance.statistics.api.deps import get_metrica_service
from app.modules.governance.statistics.api.schemas.metrica_schema import MetricaCreate, MetricaListaResponse, MetricaResponse, MetricaUpdate, MetricaValorUpdate
from app.modules.governance.statistics.application.services.metrica_service import MetricaService
from app.modules.governance.statistics.domain.enums import FonteDados, TipoMetrica
from app.modules.governance.statistics.exceptions import EstatisticaConflictError, EstatisticaNotFoundError
router = APIRouter(prefix='/metricas', tags=['Estatistica - Metricas'])

@router.post('/', response_model=MetricaResponse, status_code=status.HTTP_201_CREATED)
async def criar_metrica(data: MetricaCreate, service: MetricaService=Depends(get_metrica_service)) -> MetricaResponse:
    try:
        metrica = await service.criar_metrica(data.model_dump())
        return MetricaResponse.model_validate(metrica)
    except EstatisticaConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))

@router.get('/', response_model=MetricaListaResponse)
async def listar_metricas(tipo: TipoMetrica | None=Query(None), fonte: FonteDados | None=Query(None), pagina: int=Query(1, ge=1), tamanho_pagina: int=Query(20, ge=1, le=100), service: MetricaService=Depends(get_metrica_service)) -> MetricaListaResponse:
    offset = (pagina - 1) * tamanho_pagina
    metricas = await service.listar_metricas(tipo=tipo, fonte=fonte, limit=tamanho_pagina, offset=offset)
    return MetricaListaResponse(metricas=[MetricaResponse.model_validate(m) for m in metricas], total=len(metricas), pagina=pagina, tamanho_pagina=tamanho_pagina, filtros_aplicados={'tipo': tipo.value if tipo else None, 'fonte': fonte.value if fonte else None})

@router.get('/{metrica_id}', response_model=MetricaResponse)
async def obter_metrica(metrica_id: int, service: MetricaService=Depends(get_metrica_service)) -> MetricaResponse:
    try:
        return MetricaResponse.model_validate(await service.obter_metrica(metrica_id))
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.patch('/{metrica_id}', response_model=MetricaResponse)
async def atualizar_metrica(metrica_id: int, data: MetricaUpdate, service: MetricaService=Depends(get_metrica_service)) -> MetricaResponse:
    try:
        return MetricaResponse.model_validate(await service.atualizar_metrica(metrica_id, data.model_dump(exclude_unset=True)))
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.put('/{metrica_id}/valor', response_model=MetricaResponse)
async def atualizar_valor_metrica(metrica_id: int, data: MetricaValorUpdate, service: MetricaService=Depends(get_metrica_service)) -> MetricaResponse:
    try:
        return MetricaResponse.model_validate(await service.atualizar_valor(metrica_id, data.valor))
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{metrica_id}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_metrica(metrica_id: int, service: MetricaService=Depends(get_metrica_service)) -> None:
    try:
        await service.deletar_metrica(metrica_id)
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))