from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.modules.intelligence.defesa_consumidor.api.schemas.reclamacao_schema import ReclamacaoCreate, ReclamacaoListaResponse, ReclamacaoResponse
from app.modules.intelligence.defesa_consumidor.application.services.reclamacao_service import ReclamacaoService
from app.modules.intelligence.defesa_consumidor.infrastructure.repositories.sqlalchemy_reclamacao_repository import SQLAlchemyReclamacaoRepository
router = APIRouter(prefix='/reclamacoes', tags=['Defesa Consumidor - Reclamacoes'])

async def get_reclamacao_service(db: AsyncSession=Depends(get_db)) -> ReclamacaoService:
    repository = SQLAlchemyReclamacaoRepository(db)
    return ReclamacaoService(repository)

@router.post('/', response_model=ReclamacaoResponse, status_code=status.HTTP_201_CREATED)
async def criar_reclamacao(data: ReclamacaoCreate, service: ReclamacaoService=Depends(get_reclamacao_service)) -> ReclamacaoResponse:
    try:
        return ReclamacaoResponse.model_validate(await service.criar_reclamacao(data.model_dump()))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/', response_model=ReclamacaoListaResponse)
async def listar_reclamacoes(status_filter: str | None=Query(default=None, alias='status'), prioridade: str | None=Query(default=None), consumidor_id: int | None=Query(default=None), estabelecimento_id: int | None=Query(default=None), pagina: int=Query(default=1, ge=1), tamanho_pagina: int=Query(default=20, ge=1, le=100), service: ReclamacaoService=Depends(get_reclamacao_service)) -> ReclamacaoListaResponse:
    offset = (pagina - 1) * tamanho_pagina
    repository = service.repository
    try:
        if prioridade:
            dados = await service.listar_prioritarias(prioridade, tamanho_pagina)
        elif consumidor_id:
            dados = await service.listar_por_consumidor(consumidor_id, tamanho_pagina)
        elif estabelecimento_id:
            dados = await repository.list_by_estabelecimento(estabelecimento_id, tamanho_pagina, offset)
        elif status_filter:
            dados = await repository.list_by_status(status_filter.lower(), tamanho_pagina, offset)
        else:
            dados = await repository.list_by_status('aberta', tamanho_pagina, offset)
        reclamacoes = [ReclamacaoResponse.model_validate(item) for item in dados]
        return ReclamacaoListaResponse(reclamacoes=reclamacoes, total=len(reclamacoes), pagina=pagina, tamanho_pagina=tamanho_pagina)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{reclamacao_id}', response_model=ReclamacaoResponse)
async def obter_reclamacao(reclamacao_id: int, service: ReclamacaoService=Depends(get_reclamacao_service)) -> ReclamacaoResponse:
    try:
        return ReclamacaoResponse.model_validate(await service.obter_reclamacao(reclamacao_id))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.patch('/{reclamacao_id}/status', response_model=ReclamacaoResponse)
async def atualizar_status(reclamacao_id: int, novo_status: str=Query(...), service: ReclamacaoService=Depends(get_reclamacao_service)) -> ReclamacaoResponse:
    try:
        return ReclamacaoResponse.model_validate(await service.atualizar_status(reclamacao_id, novo_status))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{reclamacao_id}/finalizar', response_model=ReclamacaoResponse)
async def finalizar_reclamacao(reclamacao_id: int, resolvido: bool=Query(default=True), descricao_resposta: str | None=Query(default=None), service: ReclamacaoService=Depends(get_reclamacao_service)) -> ReclamacaoResponse:
    try:
        return ReclamacaoResponse.model_validate(await service.finalizar_reclamacao(reclamacao_id, resolvido, descricao_resposta))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{reclamacao_id}/escalar', response_model=ReclamacaoResponse)
async def escalar_prioridade(reclamacao_id: int, service: ReclamacaoService=Depends(get_reclamacao_service)) -> ReclamacaoResponse:
    try:
        return ReclamacaoResponse.model_validate(await service.escalar_prioridade(reclamacao_id))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.delete('/{reclamacao_id}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_reclamacao(reclamacao_id: int, service: ReclamacaoService=Depends(get_reclamacao_service)) -> None:
    deleted = await service.repository.delete(reclamacao_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Reclamacao nao encontrada')