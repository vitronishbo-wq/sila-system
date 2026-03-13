from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.modules.infrastructure_sector.meteorologia.api.deps import get_estacao_service
from app.modules.infrastructure_sector.meteorologia.api.schemas import EstacaoCreateSchema, EstacaoResponseSchema, EstacaoUpdateSchema
from app.modules.infrastructure_sector.meteorologia.application.services.estacao_service import EstacaoService
router = APIRouter(prefix='/estacoes', tags=['Meteorologia - Estacoes'])

@router.post('/', response_model=EstacaoResponseSchema, status_code=status.HTTP_201_CREATED)
async def criar_estacao(payload: EstacaoCreateSchema, service: EstacaoService=Depends(get_estacao_service)) -> EstacaoResponseSchema:
    try:
        return await service.criar_estacao(payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/', response_model=list[EstacaoResponseSchema])
async def listar_estacoes(provincia: str | None=Query(None, description='Filtro por provincia'), status_filtro: str | None=Query(None, alias='status', description='Filtro por status'), limit: int=Query(100, ge=1, le=500), offset: int=Query(0, ge=0), service: EstacaoService=Depends(get_estacao_service)) -> list[EstacaoResponseSchema]:
    try:
        return await service.listar_estacoes(provincia=provincia, status=status_filtro, limit=limit, offset=offset)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{estacao_id}', response_model=EstacaoResponseSchema)
async def obter_estacao(estacao_id: UUID, service: EstacaoService=Depends(get_estacao_service)) -> EstacaoResponseSchema:
    try:
        return await service.obter_estacao(estacao_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.put('/{estacao_id}', response_model=EstacaoResponseSchema)
async def atualizar_estacao(estacao_id: UUID, payload: EstacaoUpdateSchema, service: EstacaoService=Depends(get_estacao_service)) -> EstacaoResponseSchema:
    try:
        return await service.atualizar_estacao(estacao_id, payload.model_dump(exclude_unset=True))
    except ValueError as exc:
        status_code = status.HTTP_404_NOT_FOUND if 'nao encontrada' in str(exc).lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=str(exc))

@router.delete('/{estacao_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_estacao(estacao_id: UUID, service: EstacaoService=Depends(get_estacao_service)) -> None:
    try:
        await service.remover_estacao(estacao_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))