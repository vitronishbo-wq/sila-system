from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, status
from apps.backend.app.modules.society.assistencia_social.api.deps import get_atendimento_service
from apps.backend.app.modules.society.assistencia_social.api.endpoints._errors import raise_http_for_value_error
from apps.backend.app.modules.society.assistencia_social.api.schemas.atendimento_schema import AtendimentoCreate, AtendimentoResponse
from apps.backend.app.modules.society.assistencia_social.application.services.atendimento_service import AtendimentoService
router = APIRouter(prefix='/atendimentos', tags=['Assistencia Social - Atendimentos'])

@router.post('/', response_model=AtendimentoResponse, status_code=status.HTTP_201_CREATED)
async def registrar_atendimento(data: AtendimentoCreate, service: AtendimentoService=Depends(get_atendimento_service)) -> AtendimentoResponse:
    try:
        return await service.registrar_atendimento(beneficiario_id=data.beneficiario_id, tipo=data.tipo, descricao=data.descricao, responsavel_id=data.responsavel_id, encaminhamentos=data.encaminhamentos)
    except ValueError as exc:
        raise_http_for_value_error(exc)

@router.get('/{atendimento_id}', response_model=AtendimentoResponse)
async def obter_atendimento(atendimento_id: UUID, service: AtendimentoService=Depends(get_atendimento_service)) -> AtendimentoResponse:
    try:
        return await service.buscar_atendimento(atendimento_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)

@router.get('/', response_model=list[AtendimentoResponse])
async def listar_atendimentos(beneficiario_id: UUID | None=None, service: AtendimentoService=Depends(get_atendimento_service)) -> list[AtendimentoResponse]:
    return await service.listar_atendimentos(beneficiario_id=beneficiario_id)

@router.patch('/{atendimento_id}/encerrar', response_model=AtendimentoResponse)
async def encerrar_atendimento(atendimento_id: UUID, service: AtendimentoService=Depends(get_atendimento_service)) -> AtendimentoResponse:
    try:
        return await service.encerrar_atendimento(atendimento_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)

@router.delete('/{atendimento_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_atendimento(atendimento_id: UUID, service: AtendimentoService=Depends(get_atendimento_service)) -> None:
    try:
        await service.remover_atendimento(atendimento_id)
    except ValueError as exc:
        raise_http_for_value_error(exc)