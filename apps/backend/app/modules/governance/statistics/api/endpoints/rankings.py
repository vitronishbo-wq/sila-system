from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Query, status
from apps.backend.app.modules.governance.statistics.api.deps import get_ranking_service
from apps.backend.app.modules.governance.statistics.api.schemas.ranking_schema import RankingCreate, RankingListResponse, RankingResponse, RankingUpdate
from apps.backend.app.modules.governance.statistics.application.services.ranking_service import RankingService
from apps.backend.app.modules.governance.statistics.exceptions import EstatisticaNotFoundError
router = APIRouter(prefix='/rankings', tags=['Estatistica - Rankings'])

@router.post('/', response_model=RankingResponse, status_code=status.HTTP_201_CREATED)
async def criar_ranking(data: RankingCreate, service: RankingService=Depends(get_ranking_service)) -> RankingResponse:
    return RankingResponse.model_validate(await service.criar(data.model_dump()))

@router.get('/', response_model=RankingListResponse)
async def listar_rankings(pagina: int=Query(1, ge=1), tamanho_pagina: int=Query(20, ge=1, le=100), service: RankingService=Depends(get_ranking_service)) -> RankingListResponse:
    offset = (pagina - 1) * tamanho_pagina
    itens = await service.listar(limit=tamanho_pagina, offset=offset)
    return RankingListResponse(itens=[RankingResponse.model_validate(i) for i in itens], total=len(itens), pagina=pagina, tamanho_pagina=tamanho_pagina)

@router.get('/{ranking_id}', response_model=RankingResponse)
async def obter_ranking(ranking_id: int, service: RankingService=Depends(get_ranking_service)) -> RankingResponse:
    try:
        return RankingResponse.model_validate(await service.obter(ranking_id))
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.patch('/{ranking_id}', response_model=RankingResponse)
async def atualizar_ranking(ranking_id: int, data: RankingUpdate, service: RankingService=Depends(get_ranking_service)) -> RankingResponse:
    try:
        return RankingResponse.model_validate(await service.atualizar(ranking_id, data.model_dump(exclude_unset=True)))
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{ranking_id}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_ranking(ranking_id: int, service: RankingService=Depends(get_ranking_service)) -> None:
    try:
        await service.deletar(ranking_id)
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))