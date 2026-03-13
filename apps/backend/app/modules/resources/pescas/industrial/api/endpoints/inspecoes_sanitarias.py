from __future__ import annotations
from datetime import date
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from app.modules.resources.pescas.industrial.api.deps import get_inspecao_industrial_service
from app.modules.resources.pescas.industrial.api.schemas.inspecao_schema import InspecaoCreate, InspecaoResponse, InspecaoStatusUpdate
from app.modules.resources.pescas.industrial.application.services.inspecao_industrial_service import InspecaoIndustrialService
from app.modules.resources.pescas.industrial.domain.enums import StatusInspecao
router = APIRouter(prefix='/inspecoes-sanitarias', tags=['Pescas Industriais - Inspecoes Sanitarias'])

@router.post('/', response_model=InspecaoResponse, status_code=status.HTTP_201_CREATED)
async def agendar_inspecao(data: InspecaoCreate, service: InspecaoIndustrialService=Depends(get_inspecao_industrial_service)) -> InspecaoResponse:
    try:
        return await service.agendar_inspecao(unidade_processamento_id=data.unidade_processamento_id, data_agendada=data.data_agendada, selo_inspecao=data.selo_inspecao, fiscal_id=data.fiscal_id, lote_producao_id=data.lote_producao_id, observacoes=data.observacoes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

@router.get('/{inspecao_id}', response_model=InspecaoResponse)
async def obter_inspecao(inspecao_id: UUID, service: InspecaoIndustrialService=Depends(get_inspecao_industrial_service)) -> InspecaoResponse:
    try:
        return await service.buscar_inspecao(inspecao_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.get('/', response_model=list[InspecaoResponse])
async def listar_inspecoes(unidade_processamento_id: UUID | None=None, status_inspecao: StatusInspecao | None=None, lote_producao_id: UUID | None=None, data_inicio: date | None=None, data_fim: date | None=None, service: InspecaoIndustrialService=Depends(get_inspecao_industrial_service)) -> list[InspecaoResponse]:
    return await service.listar_inspecoes(unidade_processamento_id=unidade_processamento_id, status=status_inspecao, lote_producao_id=lote_producao_id, data_inicio=data_inicio, data_fim=data_fim)

@router.patch('/{inspecao_id}/status', response_model=InspecaoResponse)
async def atualizar_status_inspecao(inspecao_id: UUID, data: InspecaoStatusUpdate, service: InspecaoIndustrialService=Depends(get_inspecao_industrial_service)) -> InspecaoResponse:
    try:
        return await service.atualizar_status(inspecao_id=inspecao_id, status=data.status, pontuacao=data.pontuacao, aprovada=data.aprovada, inconformidades=data.inconformidades, observacoes=data.observacoes)
    except ValueError as exc:
        message = str(exc)
        code = status.HTTP_404_NOT_FOUND if 'nao encontrado' in message.lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=code, detail=message)

@router.delete('/{inspecao_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remover_inspecao(inspecao_id: UUID, service: InspecaoIndustrialService=Depends(get_inspecao_industrial_service)) -> None:
    try:
        await service.remover_inspecao(inspecao_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))