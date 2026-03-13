from __future__ import annotations
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.society.emprego.api.deps import get_certificacao_service
from apps.backend.app.modules.society.emprego.api.endpoints.certificacoes import router as certificacoes_router
from apps.backend.app.modules.society.emprego.application.services.certificacao_service import CertificacaoService
from apps.backend.app.modules.society.emprego.domain.models._workflow_record import WorkflowEmpregoRecord

@pytest.mark.asyncio
async def test_listar_certificacoes_por_cidadao():
    citizen_id = uuid4()
    records = [WorkflowEmpregoRecord(id=uuid4(), numero_processo='CERT/2026/0004', citizen_id=citizen_id, data_registro=date.today(), service_type='certificacao_profissional')]
    repository = SimpleNamespace(list_by_citizen=AsyncMock(return_value=records))
    service = CertificacaoService(repository=repository)
    result = await service.listar_por_cidadao(citizen_id, 'certificacao_profissional')
    assert result == records
    repository.list_by_citizen.assert_awaited_once_with(citizen_id, 'certificacao_profissional')

def _build_client(service) -> TestClient:
    app = FastAPI()
    app.include_router(certificacoes_router, prefix='/emprego')
    app.dependency_overrides[get_certificacao_service] = lambda: service
    return TestClient(app)

def test_endpoint_listar_certificacoes_por_cidadao_retorna_200():
    citizen_id = uuid4()
    records = [WorkflowEmpregoRecord(id=uuid4(), numero_processo='CERT/2026/0020', citizen_id=citizen_id, data_registro=date.today(), service_type='certificacao_profissional')]
    service = SimpleNamespace(listar_por_cidadao=AsyncMock(return_value=records))
    client = _build_client(service)
    response = client.get(f'/emprego/workflow/citizen/{citizen_id}')
    assert response.status_code == 200
    payload = response.json()
    assert payload[0]['numero_processo'] == 'CERT/2026/0020'