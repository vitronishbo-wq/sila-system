from __future__ import annotations

from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.backend.app.modules.economy.trade.external.api.deps import get_siscomex_drawback_service
from apps.backend.app.modules.economy.trade.external.api.endpoints.siscomex_drawback import (
    router as siscomex_drawback_router,
)
from apps.backend.app.modules.economy.trade.external.application.services import (
    SiscomexDrawbackService,
)
from apps.backend.app.modules.economy.trade.external.domain.enums import (
    StatusHabilitacao,
    TipoPessoa,
)
from apps.backend.app.modules.economy.trade.external.exceptions import (
    SiscomexDrawbackAlreadyExistsError,
    SiscomexDrawbackNotFoundError,
)
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories import (
    InMemorySiscomexDrawbackRepository,
)


@pytest.mark.asyncio
async def test_service_fluxo_principal_siscomex_drawback():
    service = SiscomexDrawbackService(repository=InMemorySiscomexDrawbackRepository())
    item = await service.solicitar(
        tipo_pessoa=TipoPessoa.JURIDICA,
        razao_social="Siscomex Drawback SA",
        cnpj_cpf="50020030000169",
        numero_processo="PROC-SISC-DRAW-2026-001",
        data_solicitacao=date(2026, 3, 15),
    )
    assert item.status == StatusHabilitacao.PENDENTE
    item = await service.rejeitar(
        item.id, data_analise=date(2026, 3, 18), motivo="Pendencia documental"
    )
    assert item.status == StatusHabilitacao.CANCELADO
    item = await service.reabrir(item.id)
    assert item.status == StatusHabilitacao.PENDENTE
    item = await service.aprovar(
        item.id,
        numero_radar="RADAR-DRAW-2026-5008",
        data_analise=date(2026, 3, 20),
        data_validade=date(2027, 3, 20),
    )
    assert item.status == StatusHabilitacao.HABILITADO


@pytest.mark.asyncio
async def test_service_detecta_processo_duplicado_siscomex_drawback():
    service = SiscomexDrawbackService(repository=InMemorySiscomexDrawbackRepository())
    payload = dict(
        tipo_pessoa=TipoPessoa.JURIDICA,
        razao_social="Duplicada Siscomex Drawback SA",
        cnpj_cpf="50020030000170",
        numero_processo="PROC-SISC-DRAW-2026-002",
        data_solicitacao=date(2026, 3, 15),
    )
    await service.solicitar(**payload)
    with pytest.raises(SiscomexDrawbackAlreadyExistsError):
        await service.solicitar(**payload)


def test_endpoint_solicitar_siscomex_drawback_retorna_201():
    service = SiscomexDrawbackService(repository=InMemorySiscomexDrawbackRepository())
    app = FastAPI()
    app.include_router(siscomex_drawback_router, prefix="/comercio_externo")
    app.dependency_overrides[get_siscomex_drawback_service] = lambda: service
    client = TestClient(app)
    response = client.post(
        "/comercio_externo/siscomex_drawback/",
        json={
            "tipo_pessoa": "juridica",
            "razao_social": "HTTP Siscomex Drawback SA",
            "cnpj_cpf": "50020030000171",
            "numero_processo": "PROC-SISC-DRAW-2026-003",
            "data_solicitacao": "2026-03-15",
        },
    )
    assert response.status_code == 201
    assert response.json()["status"] == "pendente"


def test_endpoint_obter_siscomex_drawback_retorna_404():
    service = SimpleNamespace(
        obter_por_id=AsyncMock(
            side_effect=SiscomexDrawbackNotFoundError("Siscomex Drawback nao encontrado")
        )
    )
    app = FastAPI()
    app.include_router(siscomex_drawback_router, prefix="/comercio_externo")
    app.dependency_overrides[get_siscomex_drawback_service] = lambda: service
    client = TestClient(app)
    response = client.get(f"/comercio_externo/siscomex_drawback/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Siscomex Drawback nao encontrado"
