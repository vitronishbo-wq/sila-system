from __future__ import annotations
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.public_security.api.deps import get_ocorrencia_service
from app.modules.public_security.api.schemas.ocorrencia_schema import OcorrenciaCreate, OcorrenciaResponse, OcorrenciaStatusUpdate
from app.modules.public_security.application.services.ocorrencia_service import OcorrenciaService
from app.modules.public_security.domain.enums import StatusOcorrencia, TipoOcorrencia
router = APIRouter(prefix='/ocorrencias', tags=['Seguranca Publica - Ocorrencias'])

@router.post('/', response_model=OcorrenciaResponse, status_code=status.HTTP_201_CREATED)
async def registrar_ocorrencia(data: OcorrenciaCreate, service: OcorrenciaService=Depends(get_ocorrencia_service)) -> OcorrenciaResponse:
    try:
        return await service.registrar_ocorrencia(unidade_id=data.unidade_id, tipo=data.tipo, prioridade=data.prioridade, data_ocorrencia=data.data_ocorrencia, descricao=data.descricao, municipio=data.municipio, provincia=data.provincia, policial_responsavel_id=data.policial_responsavel_id, endereco=data.endereco, vitimas=data.vitimas, suspeitos=data.suspeitos, preso_em_flagrante=data.preso_em_flagrante, observacoes=data.observacoes, citizen_id=data.citizen_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{ocorrencia_id}', response_model=OcorrenciaResponse)
async def obter_ocorrencia(ocorrencia_id: UUID, service: OcorrenciaService=Depends(get_ocorrencia_service)) -> OcorrenciaResponse:
    try:
        return await service.buscar_ocorrencia(ocorrencia_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[OcorrenciaResponse])
async def listar_ocorrencias(unidade_id: UUID | None=None, tipo: TipoOcorrencia | None=None, status_ocorrencia: StatusOcorrencia | None=None, inicio: datetime | None=None, fim: datetime | None=None, service: OcorrenciaService=Depends(get_ocorrencia_service)) -> list[OcorrenciaResponse]:
    return await service.listar_ocorrencias(unidade_id=unidade_id, tipo=tipo, status=status_ocorrencia, inicio=inicio, fim=fim)

@router.patch('/{ocorrencia_id}/status', response_model=OcorrenciaResponse)
async def atualizar_status_ocorrencia(ocorrencia_id: UUID, data: OcorrenciaStatusUpdate, service: OcorrenciaService=Depends(get_ocorrencia_service)) -> OcorrenciaResponse:
    try:
        return await service.atualizar_status(ocorrencia_id=ocorrencia_id, status=data.status, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{ocorrencia_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_ocorrencia(ocorrencia_id: UUID, service: OcorrenciaService=Depends(get_ocorrencia_service)) -> None:
    try:
        await service.remover_ocorrencia(ocorrencia_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))