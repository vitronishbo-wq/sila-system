from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.civil_protection.api.deps import get_corporacao_service
from app.modules.civil_protection.api.schemas.corporacao_schema import CorporacaoCreate, CorporacaoResponse, CorporacaoStatusUpdate
from app.modules.civil_protection.application.services.corporacao_service import CorporacaoService
from app.modules.civil_protection.domain.enums import StatusCorporacao
router = APIRouter(prefix='/corporacoes', tags=['Protecao Civil - Corporacoes'])

@router.post('/', response_model=CorporacaoResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_corporacao(data: CorporacaoCreate, service: CorporacaoService=Depends(get_corporacao_service)) -> CorporacaoResponse:
    try:
        return await service.cadastrar_corporacao(nome=data.nome, municipio=data.municipio, provincia=data.provincia, endereco=data.endereco, comandante=data.comandante, telefone=data.telefone, email=data.email, observacoes=data.observacoes, citizen_id=data.citizen_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{corporacao_id}', response_model=CorporacaoResponse)
async def obter_corporacao(corporacao_id: UUID, service: CorporacaoService=Depends(get_corporacao_service)) -> CorporacaoResponse:
    try:
        return await service.buscar_corporacao(corporacao_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[CorporacaoResponse])
async def listar_corporacoes(municipio: str | None=None, status_corporacao: StatusCorporacao | None=None, service: CorporacaoService=Depends(get_corporacao_service)) -> list[CorporacaoResponse]:
    return await service.listar_corporacoes(municipio=municipio, status=status_corporacao)

@router.patch('/{corporacao_id}/status', response_model=CorporacaoResponse)
async def atualizar_status_corporacao(corporacao_id: UUID, data: CorporacaoStatusUpdate, service: CorporacaoService=Depends(get_corporacao_service)) -> CorporacaoResponse:
    try:
        return await service.atualizar_status(corporacao_id=corporacao_id, status=data.status, motivo=data.motivo)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{corporacao_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_corporacao(corporacao_id: UUID, service: CorporacaoService=Depends(get_corporacao_service)) -> None:
    try:
        await service.remover_corporacao(corporacao_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))