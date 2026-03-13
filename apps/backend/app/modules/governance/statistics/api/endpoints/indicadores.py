from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.modules.governance.statistics.api.deps import get_indicador_service
from app.modules.governance.statistics.api.schemas.indicador_schema import IndicadorCreate, IndicadorListResponse, IndicadorResponse, IndicadorUpdate
from app.modules.governance.statistics.application.services.indicador_service import IndicadorService
from app.modules.governance.statistics.exceptions import EstatisticaNotFoundError
router = APIRouter(prefix='/indicadores', tags=['Estatistica - Indicadores'])

@router.post('/', response_model=IndicadorResponse, status_code=status.HTTP_201_CREATED)
async def criar_indicador(data: IndicadorCreate, service: IndicadorService=Depends(get_indicador_service)) -> IndicadorResponse:
    return IndicadorResponse.model_validate(await service.criar(data.model_dump()))

@router.get('/', response_model=IndicadorListResponse)
async def listar_indicadores(pagina: int=Query(1, ge=1), tamanho_pagina: int=Query(20, ge=1, le=100), service: IndicadorService=Depends(get_indicador_service)) -> IndicadorListResponse:
    offset = (pagina - 1) * tamanho_pagina
    itens = await service.listar(limit=tamanho_pagina, offset=offset)
    return IndicadorListResponse(itens=[IndicadorResponse.model_validate(i) for i in itens], total=len(itens), pagina=pagina, tamanho_pagina=tamanho_pagina)

@router.get('/{indicador_id}', response_model=IndicadorResponse)
async def obter_indicador(indicador_id: int, service: IndicadorService=Depends(get_indicador_service)) -> IndicadorResponse:
    try:
        return IndicadorResponse.model_validate(await service.obter(indicador_id))
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.patch('/{indicador_id}', response_model=IndicadorResponse)
async def atualizar_indicador(indicador_id: int, data: IndicadorUpdate, service: IndicadorService=Depends(get_indicador_service)) -> IndicadorResponse:
    try:
        return IndicadorResponse.model_validate(await service.atualizar(indicador_id, data.model_dump(exclude_unset=True)))
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{indicador_id}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_indicador(indicador_id: int, service: IndicadorService=Depends(get_indicador_service)) -> None:
    try:
        await service.deletar(indicador_id)
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))