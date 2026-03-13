from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from apps.backend.app.modules.public_security.api.deps import get_investigacao_service
from apps.backend.app.modules.public_security.api.schemas.investigacao_schema import InvestigacaoCreate, InvestigacaoResponse, InvestigacaoStatusUpdate
from apps.backend.app.modules.public_security.application.services.investigacao_service import InvestigacaoService
from apps.backend.app.modules.public_security.domain.enums import StatusInvestigacao
router = APIRouter(prefix='/investigacoes', tags=['Seguranca Publica - Investigacoes'])

@router.post('/', response_model=InvestigacaoResponse, status_code=status.HTTP_201_CREATED)
async def abrir_investigacao(data: InvestigacaoCreate, service: InvestigacaoService=Depends(get_investigacao_service)) -> InvestigacaoResponse:
    try:
        return await service.abrir_investigacao(ocorrencia_id=data.ocorrencia_id, delegado_responsavel_id=data.delegado_responsavel_id, resumo=data.resumo, observacoes=data.observacoes, citizen_id=data.citizen_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{investigacao_id}', response_model=InvestigacaoResponse)
async def obter_investigacao(investigacao_id: UUID, service: InvestigacaoService=Depends(get_investigacao_service)) -> InvestigacaoResponse:
    try:
        return await service.buscar_investigacao(investigacao_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[InvestigacaoResponse])
async def listar_investigacoes(ocorrencia_id: UUID | None=None, status_investigacao: StatusInvestigacao | None=None, service: InvestigacaoService=Depends(get_investigacao_service)) -> list[InvestigacaoResponse]:
    return await service.listar_investigacoes(ocorrencia_id=ocorrencia_id, status=status_investigacao)

@router.patch('/{investigacao_id}/status', response_model=InvestigacaoResponse)
async def atualizar_status_investigacao(investigacao_id: UUID, data: InvestigacaoStatusUpdate, service: InvestigacaoService=Depends(get_investigacao_service)) -> InvestigacaoResponse:
    try:
        return await service.atualizar_status(investigacao_id=investigacao_id, status=data.status, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete('/{investigacao_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_investigacao(investigacao_id: UUID, service: InvestigacaoService=Depends(get_investigacao_service)) -> None:
    try:
        await service.remover_investigacao(investigacao_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))