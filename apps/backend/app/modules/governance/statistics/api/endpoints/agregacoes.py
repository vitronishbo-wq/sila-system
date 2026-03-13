from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Query, status
from apps.backend.app.modules.governance.statistics.api.deps import get_agregacao_service
from apps.backend.app.modules.governance.statistics.api.schemas.agregacao_schema import AgregacaoCreate, AgregacaoListResponse, AgregacaoResponse, AgregacaoUpdate
from apps.backend.app.modules.governance.statistics.application.services.agregacao_service import AgregacaoService
from apps.backend.app.modules.governance.statistics.exceptions import EstatisticaNotFoundError
router = APIRouter(prefix='/agregacoes', tags=['Estatistica - Agregacoes'])

@router.post('/', response_model=AgregacaoResponse, status_code=status.HTTP_201_CREATED)
async def criar_agregacao(data: AgregacaoCreate, service: AgregacaoService=Depends(get_agregacao_service)) -> AgregacaoResponse:
    return AgregacaoResponse.model_validate(await service.criar(data.model_dump()))

@router.get('/', response_model=AgregacaoListResponse)
async def listar_agregacoes(pagina: int=Query(1, ge=1), tamanho_pagina: int=Query(20, ge=1, le=100), service: AgregacaoService=Depends(get_agregacao_service)) -> AgregacaoListResponse:
    offset = (pagina - 1) * tamanho_pagina
    itens = await service.listar(limit=tamanho_pagina, offset=offset)
    return AgregacaoListResponse(itens=[AgregacaoResponse.model_validate(i) for i in itens], total=len(itens), pagina=pagina, tamanho_pagina=tamanho_pagina)

@router.get('/{agregacao_id}', response_model=AgregacaoResponse)
async def obter_agregacao(agregacao_id: int, service: AgregacaoService=Depends(get_agregacao_service)) -> AgregacaoResponse:
    try:
        return AgregacaoResponse.model_validate(await service.obter(agregacao_id))
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.patch('/{agregacao_id}', response_model=AgregacaoResponse)
async def atualizar_agregacao(agregacao_id: int, data: AgregacaoUpdate, service: AgregacaoService=Depends(get_agregacao_service)) -> AgregacaoResponse:
    try:
        return AgregacaoResponse.model_validate(await service.atualizar(agregacao_id, data.model_dump(exclude_unset=True)))
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{agregacao_id}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_agregacao(agregacao_id: int, service: AgregacaoService=Depends(get_agregacao_service)) -> None:
    try:
        await service.deletar(agregacao_id)
    except EstatisticaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))