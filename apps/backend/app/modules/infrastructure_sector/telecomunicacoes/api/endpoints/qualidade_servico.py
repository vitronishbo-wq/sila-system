from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.deps import get_qualidade_servico_service
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.api.schemas.qualidade_servico_schema import QualidadeServicoCreate, QualidadeServicoResponse, QualidadeServicoStatusUpdate
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.services.qualidade_servico_service import QualidadeServicoService
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusQualidadeServico
router = APIRouter(prefix='/qualidade-servico', tags=['Telecomunicacoes - Qualidade Servico'])

@router.post('/', response_model=QualidadeServicoResponse, status_code=status.HTTP_201_CREATED)
async def registrar_medicao(data: QualidadeServicoCreate, service: QualidadeServicoService=Depends(get_qualidade_servico_service)) -> QualidadeServicoResponse:
    try:
        return await service.registrar_medicao(operadora_id=data.operadora_id, servico=data.servico, data_medicao=data.data_medicao, disponibilidade_percentual=data.disponibilidade_percentual, latencia_ms=data.latencia_ms, jitter_ms=data.jitter_ms, perda_pacotes_percentual=data.perda_pacotes_percentual, velocidade_download_mbps=data.velocidade_download_mbps, velocidade_upload_mbps=data.velocidade_upload_mbps, assinante_id=data.assinante_id, sla_id=data.sla_id, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{medicao_id}', response_model=QualidadeServicoResponse)
async def obter_medicao(medicao_id: UUID, service: QualidadeServicoService=Depends(get_qualidade_servico_service)) -> QualidadeServicoResponse:
    try:
        return await service.buscar_medicao(medicao_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[QualidadeServicoResponse])
async def listar_medicoes(operadora_id: UUID | None=None, assinante_id: UUID | None=None, status_filtro: StatusQualidadeServico | None=None, service: QualidadeServicoService=Depends(get_qualidade_servico_service)) -> list[QualidadeServicoResponse]:
    return await service.listar_medicoes(operadora_id=operadora_id, assinante_id=assinante_id, status=status_filtro)

@router.patch('/{medicao_id}/status', response_model=QualidadeServicoResponse)
async def atualizar_status_medicao(medicao_id: UUID, data: QualidadeServicoStatusUpdate, service: QualidadeServicoService=Depends(get_qualidade_servico_service)) -> QualidadeServicoResponse:
    try:
        return await service.atualizar_status(medicao_id=medicao_id, status=data.status)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{medicao_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_medicao(medicao_id: UUID, service: QualidadeServicoService=Depends(get_qualidade_servico_service)) -> None:
    try:
        await service.remover_medicao(medicao_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))