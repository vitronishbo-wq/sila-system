from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.tourism.api.deps import get_roteiro_service
from apps.backend.app.modules.tourism.api.schemas.roteiro_schema import RoteiroCreate, RoteiroResponse, RoteiroUpdate
from apps.backend.app.modules.tourism.application.services.roteiro_service import RoteiroService
router = APIRouter(prefix='/roteiros', tags=['Turismo - Roteiros'])

@router.post('/', response_model=RoteiroResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_roteiro(data: RoteiroCreate, service: RoteiroService=Depends(get_roteiro_service)) -> RoteiroResponse:
    try:
        return await service.cadastrar(titulo=data.titulo, descricao=data.descricao, municipio_origem=data.municipio_origem, provincia_origem=data.provincia_origem, duracao_horas=data.duracao_horas, pontos_parada=data.pontos_parada, acessivel=data.acessivel, valor_estimado=data.valor_estimado, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{roteiro_id}', response_model=RoteiroResponse)
async def obter_roteiro(roteiro_id: UUID, service: RoteiroService=Depends(get_roteiro_service)) -> RoteiroResponse:
    try:
        return await service.obter(roteiro_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/')
async def listar_roteiros(municipio_origem: str | None=None, ativo: bool | None=None, service: RoteiroService=Depends(get_roteiro_service)) -> list[RoteiroResponse]:
    return await service.listar(municipio_origem=municipio_origem, ativo=ativo)

@router.put('/{roteiro_id}', response_model=RoteiroResponse)
async def atualizar_roteiro(roteiro_id: UUID, data: RoteiroUpdate, service: RoteiroService=Depends(get_roteiro_service)) -> RoteiroResponse:
    try:
        return await service.atualizar(roteiro_id, titulo=data.titulo, descricao=data.descricao, municipio_origem=data.municipio_origem, provincia_origem=data.provincia_origem, duracao_horas=data.duracao_horas, pontos_parada=data.pontos_parada, acessivel=data.acessivel, valor_estimado=data.valor_estimado, observacoes=data.observacoes, ativo=data.ativo, refresh_integracoes=data.refresh_integracoes)
    except ValueError as exc:
        status_code = status.HTTP_404_NOT_FOUND if 'nao encontrado' in str(exc).lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=str(exc))

@router.delete('/{roteiro_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_roteiro(roteiro_id: UUID, service: RoteiroService=Depends(get_roteiro_service)) -> None:
    try:
        await service.remover(roteiro_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))