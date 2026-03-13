from __future__ import annotations
from datetime import date
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.society.cultura.api.deps import get_evento_cultural_service
from app.modules.society.cultura.api.schemas.evento_cultural_schema import EventoCulturalCreate, EventoCulturalResponse, EventoCulturalUpdate
from app.modules.society.cultura.application.services.evento_cultural_service import EventoCulturalService
from app.modules.society.cultura.domain.enums import StatusEventoCultural, TipoEventoCultural
router = APIRouter(prefix='/eventos-culturais', tags=['Cultura - Eventos Culturais'])

@router.post('/', response_model=EventoCulturalResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar_evento(data: EventoCulturalCreate, service: EventoCulturalService=Depends(get_evento_cultural_service)) -> EventoCulturalResponse:
    try:
        return await service.cadastrar_evento(nome=data.nome, tipo=data.tipo, descricao=data.descricao, data_inicio=data.data_inicio, data_fim=data.data_fim, local=data.local, municipio=data.municipio, provincia=data.provincia, realizador_id=data.realizador_id, atracao_turistica_id=data.atracao_turistica_id, instituicao_educacional_id=data.instituicao_educacional_id, entrada_gratuita=data.entrada_gratuita, valor_ingresso=data.valor_ingresso, publico_estimado=data.publico_estimado, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{evento_id}', response_model=EventoCulturalResponse)
async def obter_evento(evento_id: UUID, service: EventoCulturalService=Depends(get_evento_cultural_service)) -> EventoCulturalResponse:
    try:
        return await service.buscar_evento(evento_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[EventoCulturalResponse])
async def listar_eventos(tipo: TipoEventoCultural | None=None, municipio: str | None=None, status_evento: StatusEventoCultural | None=None, data_inicio: date | None=None, data_fim: date | None=None, somente_ativos: bool=True, service: EventoCulturalService=Depends(get_evento_cultural_service)) -> list[EventoCulturalResponse]:
    return await service.listar_eventos(tipo=tipo, municipio=municipio, status=status_evento, data_inicio=data_inicio, data_fim=data_fim, somente_ativos=somente_ativos)

@router.patch('/{evento_id}', response_model=EventoCulturalResponse)
async def atualizar_evento(evento_id: UUID, data: EventoCulturalUpdate, service: EventoCulturalService=Depends(get_evento_cultural_service)) -> EventoCulturalResponse:
    try:
        return await service.atualizar_evento(evento_id=evento_id, nome=data.nome, tipo=data.tipo, descricao=data.descricao, data_inicio=data.data_inicio, data_fim=data.data_fim, local=data.local, municipio=data.municipio, provincia=data.provincia, atracao_turistica_id=data.atracao_turistica_id, instituicao_educacional_id=data.instituicao_educacional_id, entrada_gratuita=data.entrada_gratuita, valor_ingresso=data.valor_ingresso, publico_estimado=data.publico_estimado, status=data.status, ativo=data.ativo, observacoes=data.observacoes)
    except ValueError as exc:
        message = str(exc).lower()
        code = status.HTTP_404_NOT_FOUND if 'nao encontrado' in message else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=str(exc))

@router.delete('/{evento_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_evento(evento_id: UUID, service: EventoCulturalService=Depends(get_evento_cultural_service)) -> None:
    try:
        await service.remover_evento(evento_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))