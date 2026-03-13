from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.society.juventude.api.deps import get_programa_service
from app.modules.society.juventude.api.schemas.programa_schema import ProgramaCreate, ProgramaResponse, ProgramaStatusUpdate
from app.modules.society.juventude.application.services.programa_service import ProgramaService
from app.modules.society.juventude.domain.enums import StatusPrograma, TipoPrograma
router = APIRouter(prefix='/programas', tags=['Juventude - Programas'])

@router.post('/', response_model=ProgramaResponse, status_code=status.HTTP_201_CREATED)
async def criar_programa(data: ProgramaCreate, service: ProgramaService=Depends(get_programa_service)) -> ProgramaResponse:
    try:
        return await service.criar_programa(nome=data.nome, tipo=data.tipo, data_inicio=data.data_inicio, data_fim=data.data_fim, vagas=data.vagas, municipio=data.municipio, provincia=data.provincia, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{programa_id}', response_model=ProgramaResponse)
async def obter_programa(programa_id: UUID, service: ProgramaService=Depends(get_programa_service)) -> ProgramaResponse:
    try:
        return await service.buscar_programa(programa_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[ProgramaResponse])
async def listar_programas(tipo: TipoPrograma | None=None, status_filtro: StatusPrograma | None=None, service: ProgramaService=Depends(get_programa_service)) -> list[ProgramaResponse]:
    return await service.listar_programas(tipo=tipo, status=status_filtro)

@router.patch('/{programa_id}/status', response_model=ProgramaResponse)
async def atualizar_status_programa(programa_id: UUID, data: ProgramaStatusUpdate, service: ProgramaService=Depends(get_programa_service)) -> ProgramaResponse:
    try:
        return await service.atualizar_status(programa_id=programa_id, status=data.status)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{programa_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_programa(programa_id: UUID, service: ProgramaService=Depends(get_programa_service)) -> None:
    try:
        await service.remover_programa(programa_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))