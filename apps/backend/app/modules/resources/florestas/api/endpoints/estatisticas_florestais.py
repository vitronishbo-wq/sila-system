from __future__ import annotations

from fastapi import APIRouter, Depends

from apps.backend.app.modules.resources.florestas.api.deps import get_estatistica_florestal_service
from apps.backend.app.modules.resources.florestas.api.schemas.estatistica_florestal_schema import (
    DashboardEstatisticoFlorestal,
    IntegracaoTransversalFlorestal,
    ResumoOperacionalFlorestal,
)
from apps.backend.app.modules.resources.florestas.application.services.estatistica_florestal_service import (
    EstatisticaFlorestalService,
)

router = APIRouter(prefix="/estatisticas-florestais", tags=["Florestas - Estatisticas Florestais"])

estatistica_florestal_service_dep = Depends(get_estatistica_florestal_service)


@router.get("/", response_model=DashboardEstatisticoFlorestal)
async def dashboard(
    service: EstatisticaFlorestalService = estatistica_florestal_service_dep,
):
    return await service.gerar_dashboard()


@router.get("/operacional", response_model=ResumoOperacionalFlorestal)
async def resumo_operacional(
    service: EstatisticaFlorestalService = estatistica_florestal_service_dep,
):
    return await service.gerar_resumo_operacional()


@router.get("/integracao", response_model=IntegracaoTransversalFlorestal)
async def integracao_transversal(
    service: EstatisticaFlorestalService = estatistica_florestal_service_dep,
):
    return await service.gerar_status_integracao()


@router.get("/relatorios/operacional", response_model=ResumoOperacionalFlorestal)
async def relatorio_operacional(
    service: EstatisticaFlorestalService = estatistica_florestal_service_dep,
):
    return await service.gerar_resumo_operacional()


@router.get("/relatorios/integracao", response_model=IntegracaoTransversalFlorestal)
async def relatorio_integracao(
    service: EstatisticaFlorestalService = estatistica_florestal_service_dep,
):
    return await service.gerar_status_integracao()