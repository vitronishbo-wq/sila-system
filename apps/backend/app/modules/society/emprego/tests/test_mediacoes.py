from __future__ import annotations
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.society.emprego.api.deps import get_mediacao_service
from apps.backend.app.modules.society.emprego.api.endpoints.mediacoes import router as mediacoes_router
from apps.backend.app.modules.society.emprego.application.services.mediacao_service import MediacaoService
from apps.backend.app.modules.society.emprego.domain.enums import WorkflowStatus
from apps.backend.app.modules.society.emprego.domain.models._workflow_record import WorkflowEmpregoRecord

@pytest.mark.asyncio
async def test_concluir_mediacao_sucesso():
    item = WorkflowEmpregoRecord(id=uuid4(), numero_processo='MEDI/2026/0003', citizen_id=uuid4(), data_registro=date.today(), service_type='mediacao', status=WorkflowStatus.EM_ANALISE)
    repository = SimpleNamespace(get_by_id=AsyncMock(return_value=item), save=AsyncMock(side_effect=lambda value: value))
    request_service = SimpleNamespace(create_request=AsyncMock(return_value=uuid4()), complete_request=AsyncMock(return_value=True))
    service = MediacaoService(repository=repository, request_service=request_service)
    updated = await service.concluir_registro(item_id=item.id, actor_id=uuid4(), observacoes='Acordo concluido')
    assert updated.status == WorkflowStatus.CONCLUIDA
    assert updated.observacoes == 'Acordo concluido'
    request_service.complete_request.assert_awaited_once()

def _build_client(service) -> TestClient:
    app = FastAPI()
    app.include_router(mediacoes_router, prefix='/emprego')
    app.dependency_overrides[get_mediacao_service] = lambda: service
    return TestClient(app)

def test_endpoint_listar_mediacoes_por_cidadao():
    citizen_id = uuid4()
    records = [WorkflowEmpregoRecord(id=uuid4(), numero_processo='MEDI/2026/0009', citizen_id=citizen_id, data_registro=date.today(), service_type='mediacao')]
    service = SimpleNamespace(listar_por_cidadao=AsyncMock(return_value=records))
    client = _build_client(service)
    response = client.get(f'/emprego/workflow/citizen/{citizen_id}')
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload[0]['service_type'] == 'mediacao'