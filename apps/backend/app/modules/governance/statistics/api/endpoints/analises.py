from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Query, status
from apps.backend.app.modules.governance.statistics.api.deps import get_analise_service
from apps.backend.app.modules.governance.statistics.api.schemas.analise_schema import AnaliseCreate, AnaliseListResponse, AnaliseResponse, AnaliseUpdate
from apps.backend.app.modules.governance.statistics.application.services.analise_service import AnaliseService
from apps.backend.app.modules.governance.statistics.exceptions import EstatisticaNotFoundError
router = APIRouter(prefix='/analises', tags=['Estatistica - Analises'])

@router.post('/', response_model=AnaliseResponse, status_code=status.HTTP_201_CREATED)
async def criar_analise(data: AnaliseCreate, service: AnaliseService=Depends(get_analise_service)) -> AnaliseResponse:
    return AnaliseResponse.model_validate(await service.criar(data.model_dump()))

@router.get('/', response_model=AnaliseListResponse)
async def listar_analises(pagina: int=Query(1, ge=1), tamanho_pagina: int=Query(20, ge=1, le=100), service: AnaliseService=Depends(get_analise_service)) -> AnaliseListResponse:
    offset = (pagina - 1) * tamanho_pagina
    itens = await service.listar(limit=tamanho_pagina, offset=offset)
    return AnaliseListResponse(itens=[AnaliseResponse.model_validate(i) for i in itens], total=len(itens), pagina=pagina, tamanho_pagina=tamanho_pagina)

@router.get('/{analise_id}', response_model=AnaliseResponse)
async def obter_analise(analise_id: int, service: AnaliseService=Depends(get_analise_service)) -> AnaliseResponse:
    try:
        return AnaliseResponse.model_validate(await service.obter(analise_id))
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.patch('/{analise_id}', response_model=AnaliseResponse)
async def atualizar_analise(analise_id: int, data: AnaliseUpdate, service: AnaliseService=Depends(get_analise_service)) -> AnaliseResponse:
    try:
        return AnaliseResponse.model_validate(await service.atualizar(analise_id, data.model_dump(exclude_unset=True)))
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{analise_id}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_analise(analise_id: int, service: AnaliseService=Depends(get_analise_service)) -> None:
    try:
        await service.deletar(analise_id)
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))