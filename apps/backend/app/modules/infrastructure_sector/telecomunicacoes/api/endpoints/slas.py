from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.deps import get_sla_service
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.schemas.sla_schema import SLACreate, SLAResponse, SLAStatusUpdate
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.sla_service import SLAService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusSLA
router = APIRouter(prefix='/slas', tags=['Telecomunicacoes - SLA'])

@router.post('/', response_model=SLAResponse, status_code=status.HTTP_201_CREATED)
async def criar_sla(data: SLACreate, service: SLAService=Depends(get_sla_service)) -> SLAResponse:
    try:
        return await service.criar_sla(operadora_id=data.operadora_id, nome=data.nome, servico=data.servico, disponibilidade_min_percentual=data.disponibilidade_min_percentual, latencia_max_ms=data.latencia_max_ms, jitter_max_ms=data.jitter_max_ms, perda_pacotes_max_percentual=data.perda_pacotes_max_percentual, velocidade_download_min_mbps=data.velocidade_download_min_mbps, velocidade_upload_min_mbps=data.velocidade_upload_min_mbps, data_inicio=data.data_inicio, data_fim=data.data_fim, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{sla_id}', response_model=SLAResponse)
async def obter_sla(sla_id: UUID, service: SLAService=Depends(get_sla_service)) -> SLAResponse:
    try:
        return await service.buscar_sla(sla_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[SLAResponse])
async def listar_slas(operadora_id: UUID | None=None, status_filtro: StatusSLA | None=None, service: SLAService=Depends(get_sla_service)) -> list[SLAResponse]:
    return await service.listar_slas(operadora_id=operadora_id, status=status_filtro)

@router.patch('/{sla_id}/status', response_model=SLAResponse)
async def atualizar_status_sla(sla_id: UUID, data: SLAStatusUpdate, service: SLAService=Depends(get_sla_service)) -> SLAResponse:
    try:
        return await service.atualizar_status(sla_id=sla_id, status=data.status)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{sla_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_sla(sla_id: UUID, service: SLAService=Depends(get_sla_service)) -> None:
    try:
        await service.remover_sla(sla_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))