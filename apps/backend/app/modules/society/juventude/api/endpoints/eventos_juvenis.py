from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.society.juventude.api.deps import get_evento_juvenil_service
from apps.backend.app.modules.society.juventude.api.schemas.evento_juvenil_schema import EventoJuvenilCreate, EventoJuvenilInscricao, EventoJuvenilResponse
from apps.backend.app.modules.society.juventude.application.services.evento_juvenil_service import EventoJuvenilService
from apps.backend.app.modules.society.juventude.domain.enums import StatusEvento
router = APIRouter(prefix='/eventos-juvenis', tags=['Juventude - Eventos Juvenis'])

@router.post('/', response_model=EventoJuvenilResponse, status_code=status.HTTP_201_CREATED)
async def criar_evento(data: EventoJuvenilCreate, service: EventoJuvenilService=Depends(get_evento_juvenil_service)) -> EventoJuvenilResponse:
    try:
        return await service.criar_evento(titulo=data.titulo, tipo_evento=data.tipo_evento, area_interesse=data.area_interesse, data_evento=data.data_evento, local=data.local, municipio=data.municipio, provincia=data.provincia, vagas=data.vagas, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{evento_id}', response_model=EventoJuvenilResponse)
async def obter_evento(evento_id: UUID, service: EventoJuvenilService=Depends(get_evento_juvenil_service)) -> EventoJuvenilResponse:
    try:
        return await service.buscar_evento(evento_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[EventoJuvenilResponse])
async def listar_eventos(status_filtro: StatusEvento | None=None, service: EventoJuvenilService=Depends(get_evento_juvenil_service)) -> list[EventoJuvenilResponse]:
    return await service.listar_eventos(status=status_filtro)

@router.patch('/{evento_id}/abrir-inscricoes', response_model=EventoJuvenilResponse)
async def abrir_inscricoes(evento_id: UUID, service: EventoJuvenilService=Depends(get_evento_juvenil_service)) -> EventoJuvenilResponse:
    try:
        return await service.abrir_inscricoes(evento_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.post('/{evento_id}/inscricoes', response_model=EventoJuvenilResponse)
async def inscrever_jovem(evento_id: UUID, data: EventoJuvenilInscricao, service: EventoJuvenilService=Depends(get_evento_juvenil_service)) -> EventoJuvenilResponse:
    try:
        return await service.inscrever_jovem(evento_id=evento_id, jovem_id=data.jovem_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.patch('/{evento_id}/concluir', response_model=EventoJuvenilResponse)
async def concluir_evento(evento_id: UUID, service: EventoJuvenilService=Depends(get_evento_juvenil_service)) -> EventoJuvenilResponse:
    try:
        return await service.concluir_evento(evento_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{evento_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_evento(evento_id: UUID, service: EventoJuvenilService=Depends(get_evento_juvenil_service)) -> None:
    try:
        await service.remover_evento(evento_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))