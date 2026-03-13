from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.civil_protection.api.deps import get_atendimento_service
from apps.backend.app.modules.civil_protection.api.schemas.atendimento_schema import AtendimentoCreate, AtendimentoFinalizacao, AtendimentoResponse, AtendimentoStatusUpdate
from apps.backend.app.modules.civil_protection.application.services.atendimento_service import AtendimentoService
from apps.backend.app.modules.civil_protection.domain.enums import StatusAtendimento
router = APIRouter(prefix='/atendimentos', tags=['Protecao Civil - Atendimentos'])

@router.post('/', response_model=AtendimentoResponse, status_code=status.HTTP_201_CREATED)
async def registrar_atendimento(data: AtendimentoCreate, service: AtendimentoService=Depends(get_atendimento_service)) -> AtendimentoResponse:
    try:
        return await service.registrar_atendimento(despacho_id=data.despacho_id, local_atendimento=data.local_atendimento, vitimas_atendidas=data.vitimas_atendidas, desalojados_atendidos=data.desalojados_atendidos, obitos_confirmados=data.obitos_confirmados, equipe_responsavel_id=data.equipe_responsavel_id, observacoes=data.observacoes, citizen_id=data.citizen_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.post('/{atendimento_id}/finalizar', response_model=AtendimentoResponse)
async def finalizar_atendimento(atendimento_id: UUID, data: AtendimentoFinalizacao, service: AtendimentoService=Depends(get_atendimento_service)) -> AtendimentoResponse:
    try:
        return await service.finalizar_atendimento(atendimento_id=atendimento_id, resumo=data.resumo, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/{atendimento_id}', response_model=AtendimentoResponse)
async def obter_atendimento(atendimento_id: UUID, service: AtendimentoService=Depends(get_atendimento_service)) -> AtendimentoResponse:
    try:
        return await service.buscar_atendimento(atendimento_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[AtendimentoResponse])
async def listar_atendimentos(ocorrencia_id: UUID | None=None, despacho_id: UUID | None=None, status_atendimento: StatusAtendimento | None=None, service: AtendimentoService=Depends(get_atendimento_service)) -> list[AtendimentoResponse]:
    return await service.listar_atendimentos(ocorrencia_id=ocorrencia_id, despacho_id=despacho_id, status=status_atendimento)

@router.patch('/{atendimento_id}/status', response_model=AtendimentoResponse)
async def atualizar_status_atendimento(atendimento_id: UUID, data: AtendimentoStatusUpdate, service: AtendimentoService=Depends(get_atendimento_service)) -> AtendimentoResponse:
    try:
        return await service.atualizar_status(atendimento_id=atendimento_id, status=data.status, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{atendimento_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_atendimento(atendimento_id: UUID, service: AtendimentoService=Depends(get_atendimento_service)) -> None:
    try:
        await service.remover_atendimento(atendimento_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))