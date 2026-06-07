from __future__ import annotations

from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.backend.app.modules.economy.trade.external.api.deps import get_drawback_service
from apps.backend.app.modules.economy.trade.external.api.endpoints.drawback import (
    router as drawback_router,
)
from apps.backend.app.modules.economy.trade.external.application.services import DrawbackService
from apps.backend.app.modules.economy.trade.external.domain.enums import (
    StatusHabilitacao,
    TipoPessoa,
)
from apps.backend.app.modules.economy.trade.external.exceptions import (
    DrawbackAlreadyExistsError,
    DrawbackNotFoundError,
)
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories import (
    InMemoryDrawbackRepository,
)


@pytest.mark.asyncio
async def test_service_fluxo_principal_drawback():
    service = DrawbackService(repository=InMemoryDrawbackRepository())
    item = await service.cadastrar(
        razao_social="Drawback Angola SA",
        cnpj_cpf="50020030000148",
        tipo_pessoa=TipoPessoa.JURIDICA,
        endereco="Av. Porto Seco",
        numero="120",
        bairro="Industrial",
        municipio="Luanda",
        provincia="Luanda",
        cep="1000-010",
    )
    assert item.status == StatusHabilitacao.PENDENTE
    item = await service.habilitar(
        item.id,
        numero_radar="RADAR-DRAW-2026-3001",
        data_habilitacao=date(2026, 3, 18),
        data_validade=date(2027, 3, 18),
    )
    assert item.status == StatusHabilitacao.HABILITADO
    item = await service.suspender(
        item.id, data_suspensao=date(2026, 7, 1), motivo="Revisao de compliance"
    )
    assert item.status == StatusHabilitacao.SUSPENSO
    item = await service.reabilitar(item.id)
    assert item.status == StatusHabilitacao.HABILITADO
    item = await service.cancelar(
        item.id, data_cancelamento=date(2026, 12, 5), motivo="Encerramento do regime"
    )
    assert item.status == StatusHabilitacao.CANCELADO


@pytest.mark.asyncio
async def test_service_detecta_cnpj_cpf_duplicado_drawback():
    service = DrawbackService(repository=InMemoryDrawbackRepository())
    payload = dict(
        razao_social="Drawback Duplicado SA",
        cnpj_cpf="50020030000149",
        tipo_pessoa=TipoPessoa.JURIDICA,
        endereco="Rua B",
        numero="2",
        bairro="Centro",
        municipio="Luanda",
        provincia="Luanda",
        cep="1000-101",
    )
    await service.cadastrar(**payload)
    with pytest.raises(DrawbackAlreadyExistsError):
        await service.cadastrar(**payload)


def test_endpoint_cadastrar_drawback_retorna_201():
    service = DrawbackService(repository=InMemoryDrawbackRepository())
    app = FastAPI()
    app.include_router(drawback_router, prefix="/comercio_externo")
    app.dependency_overrides[get_drawback_service] = lambda: service
    client = TestClient(app)
    response = client.post(
        "/comercio_externo/drawback/",
        json={
            "razao_social": "Drawback HTTP SA",
            "cnpj_cpf": "50020030000150",
            "tipo_pessoa": "juridica",
            "endereco": "Rua Porto",
            "numero": "15",
            "bairro": "Portuario",
            "municipio": "Lobito",
            "provincia": "Benguela",
            "cep": "2000-500",
        },
    )
    assert response.status_code == 201
    assert response.json()["status"] == "pendente"


def test_endpoint_obter_drawback_retorna_404():
    service = SimpleNamespace(
        obter_por_id=AsyncMock(side_effect=DrawbackNotFoundError("Drawback nao encontrado"))
    )
    app = FastAPI()
    app.include_router(drawback_router, prefix="/comercio_externo")
    app.dependency_overrides[get_drawback_service] = lambda: service
    client = TestClient(app)
    response = client.get(f"/comercio_externo/drawback/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Drawback nao encontrado"
