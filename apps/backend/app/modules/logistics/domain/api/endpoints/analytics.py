from __future__ import annotations
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends
from app.modules.logistics.api.deps import get_operacao_analytics_service
from app.modules.logistics.api.schemas.analytics_schema import DemandaOperacionalResponse, QualidadeServicoResponse
from app.modules.logistics.application.services import OperacaoAnalyticsService
router = APIRouter(prefix='/analytics', tags=['Transportes Logistica - Analytics'])

@router.get('/demanda', response_model=DemandaOperacionalResponse)
async def calcular_demanda(linha_id: UUID | None=None, data_inicio: datetime | None=None, data_fim: datetime | None=None, service: OperacaoAnalyticsService=Depends(get_operacao_analytics_service)):
    return await service.calcular_demanda(linha_id=linha_id, data_inicio=data_inicio, data_fim=data_fim)

@router.get('/qualidade', response_model=QualidadeServicoResponse)
async def calcular_qualidade(linha_id: UUID | None=None, data_inicio: datetime | None=None, data_fim: datetime | None=None, service: OperacaoAnalyticsService=Depends(get_operacao_analytics_service)):
    return await service.calcular_qualidade(linha_id=linha_id, data_inicio=data_inicio, data_fim=data_fim)
