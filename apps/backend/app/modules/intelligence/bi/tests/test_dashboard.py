from __future__ import annotations
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.intelligence.bi.api.deps import get_dashboard_service
from apps.backend.app.modules.intelligence.bi.api.router import router as bi_router
from apps.backend.app.modules.intelligence.bi.application.services.dashboard_service import DashboardService
from apps.backend.app.modules.intelligence.bi.integrations.data_sources import DataSources

@pytest.mark.asyncio
@pytest.mark.integration
async def test_dashboard_executivo_retorna_consolidado_com_fontes_reais(db_session) -> None:
    sources = DataSources.from_session(db_session)
    service = DashboardService(data_sources=sources)
    payload = await service.get_dashboard_executivo(data_ref=date.today())
    assert 'reference_date' in payload
    assert 'generated_at' in payload
    assert 'summary' in payload
    assert 'domains' in payload
    assert isinstance(payload['domains'], dict)
    assert set(service.available_domains()) >= {'financas', 'financas_publicas', 'service_requests'}

@pytest.mark.asyncio
async def test_dashboard_domain_levanta_erro_quando_fonte_nao_existe() -> None:
    service = DashboardService(data_sources=DataSources(clients={}))
    with pytest.raises(KeyError):
        await service.get_dashboard_domain(domain='educacao', data_ref=date.today())

def _build_client(dashboard_service) -> TestClient:
    app = FastAPI()
    app.include_router(bi_router, prefix='/v1')
    app.dependency_overrides[get_dashboard_service] = lambda: dashboard_service
    return TestClient(app)

def test_dashboard_endpoint_retorna_503_quando_fonte_indisponivel() -> None:
    service = SimpleNamespace(has_domain_source=lambda _: False, get_dashboard_domain=AsyncMock())
    client = _build_client(service)
    response = client.get('/v1/bi/dashboards/educacao')
    assert response.status_code == 503
    assert "Fonte de dados indisponivel para o dominio 'educacao'" in response.json()['detail']
    service.get_dashboard_domain.assert_not_awaited()