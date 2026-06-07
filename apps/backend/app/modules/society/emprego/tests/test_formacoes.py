from __future__ import annotations

from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.backend.app.modules.society.emprego.api.deps import get_formacao_service
from apps.backend.app.modules.society.emprego.api.endpoints.formacoes import (
    router as formacoes_router,
)
from apps.backend.app.modules.society.emprego.application.services.formacao_service import (
    FormacaoService,
)
from apps.backend.app.modules.society.emprego.domain.enums import WorkflowStatus
from apps.backend.app.modules.society.emprego.domain.models._workflow_record import (
    WorkflowEmpregoRecord,
)


@pytest.mark.asyncio
async def test_cancelar_formacao_define_status_e_motivo():
    item = WorkflowEmpregoRecord(
        id=uuid4(),
        numero_processo="FORM/2026/0008",
        citizen_id=uuid4(),
        data_registro=date.today(),
        service_type="formacao_profissional",
    )
    repository = SimpleNamespace(
        get_by_id=AsyncMock(return_value=item), save=AsyncMock(side_effect=lambda value: value)
    )
    request_service = SimpleNamespace(
        create_request=AsyncMock(return_value=uuid4()),
        complete_request=AsyncMock(return_value=True),
    )
    service = FormacaoService(repository=repository, request_service=request_service)
    updated = await service.cancelar_registro(
        item_id=item.id, actor_id=uuid4(), motivo="Documentacao incompleta"
    )
    assert updated.status == WorkflowStatus.CANCELADA
    assert updated.observacoes == "Documentacao incompleta"
    request_service.complete_request.assert_awaited_once()


def _build_client(service) -> TestClient:
    app = FastAPI()
    app.include_router(formacoes_router, prefix="/emprego")
    app.dependency_overrides[get_formacao_service] = lambda: service
    return TestClient(app)


def test_endpoint_cancelar_formacao_retorna_200():
    item_id = uuid4()
    item = WorkflowEmpregoRecord(
        id=item_id,
        numero_processo="FORM/2026/0010",
        citizen_id=uuid4(),
        data_registro=date.today(),
        service_type="formacao_profissional",
        status=WorkflowStatus.CANCELADA,
        observacoes="Cancelada",
    )
    service = SimpleNamespace(cancelar_registro=AsyncMock(return_value=item))
    client = _build_client(service)
    response = client.post(
        f"/emprego/workflow/{item_id}/cancelar",
        json={"actor_id": str(uuid4()), "motivo": "Cancelada"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "cancelada"
