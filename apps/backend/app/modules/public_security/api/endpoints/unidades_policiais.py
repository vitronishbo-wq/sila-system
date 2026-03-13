from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.public_security.api.deps import get_unidade_policial_service
from app.modules.public_security.api.schemas.unidade_policial_schema import UnidadePolicialCreate, UnidadePolicialResponse, UnidadePolicialStatusUpdate
from app.modules.public_security.application.services.unidade_policial_service import UnidadePolicialService
from app.modules.public_security.domain.enums import StatusUnidadePolicial
router = APIRouter(prefix='/unidades-policiais', tags=['Seguranca Publica - Unidades'])

@router.post('/', response_model=UnidadePolicialResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_unidade(data: UnidadePolicialCreate, service: UnidadePolicialService=Depends(get_unidade_policial_service)) -> UnidadePolicialResponse:
    try:
        return await service.cadastrar_unidade(nome=data.nome, tipo=data.tipo, municipio=data.municipio, provincia=data.provincia, endereco=data.endereco, comandante=data.comandante, telefone=data.telefone, email=data.email, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{unidade_id}', response_model=UnidadePolicialResponse)
async def obter_unidade(unidade_id: UUID, service: UnidadePolicialService=Depends(get_unidade_policial_service)) -> UnidadePolicialResponse:
    try:
        return await service.buscar_unidade(unidade_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[UnidadePolicialResponse])
async def listar_unidades(municipio: str | None=None, status_unidade: StatusUnidadePolicial | None=None, service: UnidadePolicialService=Depends(get_unidade_policial_service)) -> list[UnidadePolicialResponse]:
    return await service.listar_unidades(municipio=municipio, status=status_unidade)

@router.patch('/{unidade_id}/status', response_model=UnidadePolicialResponse)
async def atualizar_status_unidade(unidade_id: UUID, data: UnidadePolicialStatusUpdate, service: UnidadePolicialService=Depends(get_unidade_policial_service)) -> UnidadePolicialResponse:
    try:
        return await service.atualizar_status(unidade_id=unidade_id, status=data.status, motivo=data.motivo)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{unidade_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_unidade(unidade_id: UUID, service: UnidadePolicialService=Depends(get_unidade_policial_service)) -> None:
    try:
        await service.remover_unidade(unidade_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))