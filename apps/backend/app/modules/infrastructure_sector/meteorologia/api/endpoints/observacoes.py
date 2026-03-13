from __future__ import annotations
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from apps.backend.app.modules.infrastructure_sector.meteorologia.api.deps import get_processamento_service
from apps.backend.app.modules.infrastructure_sector.meteorologia.api.schemas import ObservacaoCreateSchema, ObservacaoResponseSchema
from apps.backend.app.modules.infrastructure_sector.meteorologia.application.services.processamento_service import ProcessamentoService
from apps.backend.app.modules.infrastructure_sector.meteorologia.domain.models import ObservacaoMeteorologica
router = APIRouter(prefix='/observacoes', tags=['Meteorologia - Observacoes'])

@router.post('/', response_model=ObservacaoResponseSchema, status_code=status.HTTP_201_CREATED)
async def criar_observacao(payload: ObservacaoCreateSchema, service: ProcessamentoService=Depends(get_processamento_service)) -> ObservacaoResponseSchema:
    observacao = ObservacaoMeteorologica(estacao_id=payload.estacao_id, data_observacao=payload.data_observacao, temperatura=payload.temperatura, humidade=payload.humidade, pressao=payload.pressao, velocidade_vento=payload.velocidade_vento, direcao_vento=payload.direcao_vento, precipitacao=payload.precipitacao, radiacao_solar=payload.radiacao_solar, tipo=payload.tipo, metadata=payload.metadata)
    resultado = await service.processar_observacao(observacao)
    if not resultado['sucesso']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'erros': resultado['erros'], 'warnings': resultado['warnings']})
    persisted: ObservacaoMeteorologica = resultado['observacao'] or observacao
    return persisted.to_dict()

@router.get('/alertas/recentes', response_model=list[ObservacaoResponseSchema])
async def listar_observacoes_com_alertas(start_date: datetime | None=Query(None), end_date: datetime | None=Query(None), limit: int=Query(50, ge=1, le=200), service: ProcessamentoService=Depends(get_processamento_service)) -> list[ObservacaoResponseSchema]:
    observacoes = await service.listar_observacoes_com_alertas(start_date=start_date, end_date=end_date, limit=limit)
    return [obs.to_dict() for obs in observacoes]

@router.get('/estacao/{estacao_id}', response_model=list[ObservacaoResponseSchema])
async def listar_observacoes_estacao(estacao_id: UUID, start_date: datetime | None=Query(None), end_date: datetime | None=Query(None), limit: int=Query(100, ge=1, le=1000), service: ProcessamentoService=Depends(get_processamento_service)) -> list[ObservacaoResponseSchema]:
    observacoes = await service.listar_observacoes_estacao(estacao_id=estacao_id, start_date=start_date, end_date=end_date, limit=limit)
    return [obs.to_dict() for obs in observacoes]

@router.get('/{observacao_id}', response_model=ObservacaoResponseSchema)
async def obter_observacao(observacao_id: UUID, service: ProcessamentoService=Depends(get_processamento_service)) -> ObservacaoResponseSchema:
    try:
        observacao = await service.obter_observacao(observacao_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return observacao.to_dict()