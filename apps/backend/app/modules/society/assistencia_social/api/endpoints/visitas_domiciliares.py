from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, status
from app.modules.society.assistencia_social.api.deps import get_visita_domiciliar_service
from app.modules.society.assistencia_social.api.endpoints._errors import raise_http_for_value_error
from app.modules.society.assistencia_social.api.schemas.visita_domiciliar_schema import VisitaDomiciliarCreate, VisitaDomiciliarResponse
from app.modules.society.assistencia_social.application.services.visita_domiciliar_service import VisitaDomiciliarService
router = APIRouter(prefix='/visitas-domiciliares', tags=['Assistencia Social - Visitas Domiciliares'])

@router.post('/', response_model=VisitaDomiciliarResponse, status_code=status.HTTP_201_CREATED)
async def registrar_visita_domiciliar(data: VisitaDomiciliarCreate, service: VisitaDomiciliarService=Depends(get_visita_domiciliar_service)) -> VisitaDomiciliarResponse:
    try:
        return await service.registrar_visita(beneficiario_id=data.beneficiario_id, assistente_social_id=data.assistente_social_id, condicoes_moradia=data.condicoes_moradia, observacoes=data.observacoes, recomendacoes=data.recomendacoes, resultado=data.resultado)
    except ValueError as exc:
        raise_http_for_value_error(exc)

@router.get('/{visita_id}', response_model=VisitaDomiciliarResponse)
async def obter_visita_domiciliar(visita_id: UUID, service: VisitaDomiciliarService=Depends(get_visita_domiciliar_service)) -> VisitaDomiciliarResponse:
    try:
        return await service.buscar_visita(visita_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)

@router.get('/', response_model=list[VisitaDomiciliarResponse])
async def listar_visitas_domiciliares(beneficiario_id: UUID | None=None, service: VisitaDomiciliarService=Depends(get_visita_domiciliar_service)) -> list[VisitaDomiciliarResponse]:
    return await service.listar_visitas(beneficiario_id=beneficiario_id)

@router.delete('/{visita_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_visita_domiciliar(visita_id: UUID, service: VisitaDomiciliarService=Depends(get_visita_domiciliar_service)) -> None:
    try:
        await service.remover_visita(visita_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)