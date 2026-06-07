from __future__ import annotations

from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.backend.app.modules.economy.trade.external.api.deps import (
    get_cancelamento_radar_service,
    get_suspensao_radar_service,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints.cancelamento_radar import (
    router as cancelamento_radar_router,
)
from apps.backend.app.modules.economy.trade.external.api.endpoints.suspensao_radar import (
    router as suspensao_radar_router,
)
from apps.backend.app.modules.economy.trade.external.application.services import (
    CancelamentoRadarService,
    SuspensaoRadarService,
)
from apps.backend.app.modules.economy.trade.external.domain.enums import (
    StatusHabilitacao,
    TipoPessoa,
)
from apps.backend.app.modules.economy.trade.external.exceptions import (
    CancelamentoRadarAlreadyExistsError,
    CancelamentoRadarNotFoundError,
    SuspensaoRadarAlreadyExistsError,
    SuspensaoRadarNotFoundError,
)
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories import (
    InMemoryCancelamentoRadarRepository,
    InMemorySuspensaoRadarRepository,
)

CASES = (
    {
        "id": "cancelamento_radar",
        "service_cls": CancelamentoRadarService,
        "repository_cls": InMemoryCancelamentoRadarRepository,
        "dependency": get_cancelamento_radar_service,
        "router": cancelamento_radar_router,
        "already_exists_error_cls": CancelamentoRadarAlreadyExistsError,
        "not_found_error_cls": CancelamentoRadarNotFoundError,
        "base_url": "/comercio_externo/cancelamento_radar",
        "processo": "PROC-CAN-RADAR-2026-001",
        "cnpj": "50020030000143",
        "expected_status_after_approve": StatusHabilitacao.CANCELADO,
    },
    {
        "id": "suspensao_radar",
        "service_cls": SuspensaoRadarService,
        "repository_cls": InMemorySuspensaoRadarRepository,
        "dependency": get_suspensao_radar_service,
        "router": suspensao_radar_router,
        "already_exists_error_cls": SuspensaoRadarAlreadyExistsError,
        "not_found_error_cls": SuspensaoRadarNotFoundError,
        "base_url": "/comercio_externo/suspensao_radar",
        "processo": "PROC-SUS-RADAR-2026-001",
        "cnpj": "50020030000144",
        "expected_status_after_approve": StatusHabilitacao.SUSPENSO,
    },
)


@pytest.mark.parametrize("case", CASES, ids=[case["id"] for case in CASES])
@pytest.mark.asyncio
async def test_service_fluxo_principal_processo_radar(case):
    service = case["service_cls"](repository=case["repository_cls"]())
    item = await service.solicitar(
        tipo_pessoa=TipoPessoa.JURIDICA,
        razao_social=f"Empresa {case['id']}",
        cnpj_cpf=case["cnpj"],
        numero_processo=case["processo"],
        data_solicitacao=date(2026, 3, 15),
    )
    assert item.status == StatusHabilitacao.PENDENTE
    item = await service.rejeitar(
        item.id, data_analise=date(2026, 3, 16), motivo="Pendencia de documentacao"
    )
    assert item.status == StatusHabilitacao.CANCELADO
    item = await service.reabrir(item.id)
    assert item.status == StatusHabilitacao.PENDENTE
    item = await service.aprovar(
        item.id,
        numero_radar="RADAR-2026-7000",
        data_analise=date(2026, 3, 17),
        data_validade=date(2027, 3, 17),
    )
    assert item.status == case["expected_status_after_approve"]


@pytest.mark.parametrize("case", CASES, ids=[case["id"] for case in CASES])
@pytest.mark.asyncio
async def test_service_detecta_processo_duplicado_processo_radar(case):
    service = case["service_cls"](repository=case["repository_cls"]())
    payload = dict(
        tipo_pessoa=TipoPessoa.JURIDICA,
        razao_social=f"Duplicada {case['id']}",
        cnpj_cpf=case["cnpj"],
        numero_processo=case["processo"],
        data_solicitacao=date(2026, 3, 15),
    )
    await service.solicitar(**payload)
    with pytest.raises(case["already_exists_error_cls"]):
        await service.solicitar(**payload)


@pytest.mark.parametrize("case", CASES, ids=[case["id"] for case in CASES])
def test_endpoint_solicitar_retorna_201_processo_radar(case):
    service = case["service_cls"](repository=case["repository_cls"]())
    app = FastAPI()
    app.include_router(case["router"], prefix="/comercio_externo")
    app.dependency_overrides[case["dependency"]] = lambda: service
    client = TestClient(app)
    response = client.post(
        f"{case['base_url']}/",
        json={
            "tipo_pessoa": "juridica",
            "razao_social": f"HTTP {case['id']}",
            "cnpj_cpf": case["cnpj"],
            "numero_processo": case["processo"],
            "data_solicitacao": "2026-03-15",
        },
    )
    assert response.status_code == 201
    assert response.json()["status"] == "pendente"


@pytest.mark.parametrize("case", CASES, ids=[case["id"] for case in CASES])
def test_endpoint_obter_retorna_404_processo_radar(case):
    service = SimpleNamespace(
        obter_por_id=AsyncMock(
            side_effect=case["not_found_error_cls"]("Processo de radar nao encontrado")
        )
    )
    app = FastAPI()
    app.include_router(case["router"], prefix="/comercio_externo")
    app.dependency_overrides[case["dependency"]] = lambda: service
    client = TestClient(app)
    response = client.get(f"{case['base_url']}/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Processo de radar nao encontrado"
