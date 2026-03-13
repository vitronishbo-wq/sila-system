from __future__ import annotations
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.intelligence.bi.api.deps import get_kpi_service
from app.modules.intelligence.bi.api.router import router as bi_router
from app.modules.intelligence.bi.application.services.kpi_service import KPIService
from app.modules.intelligence.bi.integrations.data_sources import DataSources

@pytest.mark.asyncio
@pytest.mark.integration
async def test_kpi_service_consolidado_com_data_sources_reais(db_session) -> None:
    service = KPIService(data_sources=DataSources.from_session(db_session))
    payload = await service.get_consolidated_kpis(data_ref=date.today())
    assert 'reference_date' in payload
    assert 'domains' in payload
    assert isinstance(payload['domains'], dict)
    assert 'financas' in service.available_domains()
    assert 'financas_publicas' in service.available_domains()

def _build_client(kpi_service) -> TestClient:
    app = FastAPI()
    app.include_router(bi_router, prefix='/v1')
    app.dependency_overrides[get_kpi_service] = lambda: kpi_service
    return TestClient(app)

def test_kpis_endpoint_retorna_503_quando_fonte_indisponivel() -> None:
    service = SimpleNamespace(has_domain_source=lambda _: False, get_domain_kpis=AsyncMock())
    client = _build_client(service)
    response = client.get('/v1/bi/kpis/domain/educacao')
    assert response.status_code == 503
    assert "Fonte de dados indisponivel para o dominio 'educacao'" in response.json()['detail']
    service.get_domain_kpis.assert_not_awaited()

def test_kpis_endpoint_dominio_delega_para_servico() -> None:
    service = SimpleNamespace(has_domain_source=lambda _: True, get_domain_kpis=AsyncMock(return_value={'domain': 'educacao', 'reference_date': '2026-03-04', 'generated_at': '2026-03-04T00:00:00', 'metrics': {'matriculas_total': 10}, 'metric_count': 1}))
    client = _build_client(service)
    response = client.get('/v1/bi/kpis/educacao')
    assert response.status_code == 200
    assert response.json()['domain'] == 'educacao'
    service.get_domain_kpis.assert_awaited_once()