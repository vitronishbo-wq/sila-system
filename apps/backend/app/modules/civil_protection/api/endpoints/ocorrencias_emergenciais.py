from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.civil_protection.api.deps import get_ocorrencia_emergencial_service
from apps.backend.app.modules.civil_protection.api.schemas.ocorrencia_emergencial_schema import OcorrenciaEmergencialCreate, OcorrenciaEmergencialResponse, OcorrenciaEmergencialStatusUpdate
from apps.backend.app.modules.civil_protection.application.services.ocorrencia_emergencial_service import OcorrenciaEmergencialService
from apps.backend.app.modules.civil_protection.domain.enums import StatusOcorrenciaEmergencial, TipoOcorrenciaEmergencial
router = APIRouter(prefix='/ocorrencias-emergenciais', tags=['Protecao Civil - Ocorrencias Emergenciais'])

@router.post('/', response_model=OcorrenciaEmergencialResponse, status_code=status.HTTP_201_CREATED)
async def registrar_ocorrencia(data: OcorrenciaEmergencialCreate, service: OcorrenciaEmergencialService=Depends(get_ocorrencia_emergencial_service)) -> OcorrenciaEmergencialResponse:
    try:
        return await service.registrar_ocorrencia(corporacao_id=data.corporacao_id, tipo=data.tipo, prioridade=data.prioridade, data_ocorrencia=data.data_ocorrencia, descricao=data.descricao, municipio=data.municipio, provincia=data.provincia, bombeiro_responsavel_id=data.bombeiro_responsavel_id, endereco=data.endereco, vitimas=data.vitimas, desalojados=data.desalojados, obitos=data.obitos, observacoes=data.observacoes, citizen_id=data.citizen_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{ocorrencia_id}', response_model=OcorrenciaEmergencialResponse)
async def obter_ocorrencia(ocorrencia_id: UUID, service: OcorrenciaEmergencialService=Depends(get_ocorrencia_emergencial_service)) -> OcorrenciaEmergencialResponse:
    try:
        return await service.buscar_ocorrencia(ocorrencia_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[OcorrenciaEmergencialResponse])
async def listar_ocorrencias(corporacao_id: UUID | None=None, tipo_ocorrencia: TipoOcorrenciaEmergencial | None=None, status_ocorrencia: StatusOcorrenciaEmergencial | None=None, service: OcorrenciaEmergencialService=Depends(get_ocorrencia_emergencial_service)) -> list[OcorrenciaEmergencialResponse]:
    return await service.listar_ocorrencias(corporacao_id=corporacao_id, tipo=tipo_ocorrencia, status=status_ocorrencia)

@router.patch('/{ocorrencia_id}/status', response_model=OcorrenciaEmergencialResponse)
async def atualizar_status_ocorrencia(ocorrencia_id: UUID, data: OcorrenciaEmergencialStatusUpdate, service: OcorrenciaEmergencialService=Depends(get_ocorrencia_emergencial_service)) -> OcorrenciaEmergencialResponse:
    try:
        return await service.atualizar_status(ocorrencia_id=ocorrencia_id, status=data.status, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{ocorrencia_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_ocorrencia(ocorrencia_id: UUID, service: OcorrenciaEmergencialService=Depends(get_ocorrencia_emergencial_service)) -> None:
    try:
        await service.remover_ocorrencia(ocorrencia_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))