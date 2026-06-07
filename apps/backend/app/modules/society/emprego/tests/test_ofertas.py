from __future__ import annotations

from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.backend.app.modules.society.emprego.api.deps import get_oferta_service
from apps.backend.app.modules.society.emprego.api.endpoints.ofertas import router as ofertas_router
from apps.backend.app.modules.society.emprego.application.services.oferta_service import (
    OfertaService,
)
from apps.backend.app.modules.society.emprego.domain.enums import WorkflowStatus
from apps.backend.app.modules.society.emprego.domain.models._workflow_record import (
    WorkflowEmpregoRecord,
)


@pytest.mark.asyncio
async def test_criar_oferta_sucesso():
    citizen_id = uuid4()
    repository = SimpleNamespace(
        exists_active_for_citizen=AsyncMock(return_value=False),
        next_numero_processo=AsyncMock(return_value="OFER/2026/0001"),
        save=AsyncMock(side_effect=lambda item: item),
    )
    citizen_service = SimpleNamespace(is_citizen_active=AsyncMock(return_value=True))
    request_service = SimpleNamespace(
        create_request=AsyncMock(return_value=uuid4()),
        complete_request=AsyncMock(return_value=True),
    )
    service = OfertaService(
        repository=repository, citizen_service=citizen_service, request_service=request_service
    )
    record = await service.criar_registro(
        service_type="oferta_emprego",
        citizen_id=citizen_id,
        observacoes="Oferta para atendimento geral",
        metadata={"setor": "servicos"},
    )
    assert record.numero_processo == "OFER/2026/0001"
    assert record.status == WorkflowStatus.PENDENTE
    repository.next_numero_processo.assert_awaited_once_with(date.today().year, "OFER")
    request_service.create_request.assert_awaited_once()


def _build_client(service) -> TestClient:
    app = FastAPI()
    app.include_router(ofertas_router, prefix="/emprego")
    app.dependency_overrides[get_oferta_service] = lambda: service
    return TestClient(app)


def test_endpoint_criar_oferta_retorna_201():
    citizen_id = uuid4()
    item = WorkflowEmpregoRecord(
        id=uuid4(),
        numero_processo="OFER/2026/0004",
        citizen_id=citizen_id,
        data_registro=date.today(),
        service_type="oferta_emprego",
    )
    service = SimpleNamespace(criar_registro=AsyncMock(return_value=item))
    client = _build_client(service)
    response = client.post(
        "/emprego/ofertas",
        json={
            "citizen_id": str(citizen_id),
            "observacoes": "Oferta publica",
            "metadata": {"setor": "servicos"},
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["numero_processo"] == "OFER/2026/0004"
    assert body["service_type"] == "oferta_emprego"


def test_endpoint_concluir_oferta_retorna_200():
    item_id = uuid4()
    citizen_id = uuid4()
    concluido = WorkflowEmpregoRecord(
        id=item_id,
        numero_processo="OFER/2026/0004",
        citizen_id=citizen_id,
        data_registro=date.today(),
        service_type="oferta_emprego",
        status=WorkflowStatus.CONCLUIDA,
        observacoes="Concluida no portal",
    )
    service = SimpleNamespace(concluir_registro=AsyncMock(return_value=concluido))
    client = _build_client(service)
    response = client.post(
        f"/emprego/workflow/{item_id}/concluir",
        json={"actor_id": str(uuid4()), "observacoes": "Concluida no portal"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "concluida"
