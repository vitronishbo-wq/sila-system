from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Query, status
from apps.backend.app.modules.governance.statistics.api.deps import get_alerta_service
from apps.backend.app.modules.governance.statistics.api.schemas.alerta_schema import AlertaCreate, AlertaListResponse, AlertaResponse, AlertaUpdate
from apps.backend.app.modules.governance.statistics.application.services.alerta_service import AlertaService
from apps.backend.app.modules.governance.statistics.exceptions import EstatisticaNotFoundError
router = APIRouter(prefix='/alertas', tags=['Estatistica - Alertas'])

@router.post('/', response_model=AlertaResponse, status_code=status.HTTP_201_CREATED)
async def criar_alerta(data: AlertaCreate, service: AlertaService=Depends(get_alerta_service)) -> AlertaResponse:
    return AlertaResponse.model_validate(await service.criar(data.model_dump()))

@router.get('/', response_model=AlertaListResponse)
async def listar_alertas(pagina: int=Query(1, ge=1), tamanho_pagina: int=Query(20, ge=1, le=100), service: AlertaService=Depends(get_alerta_service)) -> AlertaListResponse:
    offset = (pagina - 1) * tamanho_pagina
    itens = await service.listar(limit=tamanho_pagina, offset=offset)
    return AlertaListResponse(itens=[AlertaResponse.model_validate(i) for i in itens], total=len(itens), pagina=pagina, tamanho_pagina=tamanho_pagina)

@router.get('/{alerta_id}', response_model=AlertaResponse)
async def obter_alerta(alerta_id: int, service: AlertaService=Depends(get_alerta_service)) -> AlertaResponse:
    try:
        return AlertaResponse.model_validate(await service.obter(alerta_id))
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.patch('/{alerta_id}', response_model=AlertaResponse)
async def atualizar_alerta(alerta_id: int, data: AlertaUpdate, service: AlertaService=Depends(get_alerta_service)) -> AlertaResponse:
    try:
        return AlertaResponse.model_validate(await service.atualizar(alerta_id, data.model_dump(exclude_unset=True)))
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{alerta_id}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_alerta(alerta_id: int, service: AlertaService=Depends(get_alerta_service)) -> None:
    try:
        await service.deletar(alerta_id)
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))