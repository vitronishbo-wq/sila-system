from __future__ import annotations
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.infrastructure.api.deps import get_dashboard_query_service
from apps.backend.app.modules.infrastructure.api.router import router as obras_publicas_router

def test_dashboard_endpoint_consulta_read_model_por_tenant_header():
    row = SimpleNamespace(obra_id='obra-1', tenant_id='tenant-obras', codigo='OBR/2026/000001', status='EM_EXECUCAO', valor_total=Decimal('1000.00'), valor_executado=Decimal('250.00'), percentual_execucao=Decimal('25.00'))
    query_service = SimpleNamespace(listar_obras=AsyncMock(return_value=[row]))
    app = FastAPI()
    app.include_router(obras_publicas_router)
    app.dependency_overrides[get_dashboard_query_service] = lambda: query_service
    client = TestClient(app)
    response = client.get('/obras-publicas/dashboard/obras', headers={'X-Tenant-ID': 'tenant-obras'})
    assert response.status_code == 200
    assert response.json()[0]['obra_id'] == 'obra-1'
    assert str(response.json()[0]['percentual_execucao']) in {'25.00', '25.0', '25'}
    query_service.listar_obras.assert_awaited_once_with(tenant_id='tenant-obras')
