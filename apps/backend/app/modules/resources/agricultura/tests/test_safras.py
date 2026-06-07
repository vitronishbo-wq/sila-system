from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.backend.app.modules.resources.agricultura.api.deps import get_safra_service
from apps.backend.app.modules.resources.agricultura.api.endpoints.safras import (
    router as safras_router,
)
from apps.backend.app.modules.resources.agricultura.application.services.producao_service import (
    ProducaoService,
)
from apps.backend.app.modules.resources.agricultura.application.services.propriedade_service import (
    PropriedadeService,
)
from apps.backend.app.modules.resources.agricultura.application.services.safra_service import (
    SafraService,
)
from apps.backend.app.modules.resources.agricultura.domain.enums import (
    StatusSafra,
    TipoCultura,
    TipoPropriedade,
)
from apps.backend.app.modules.resources.agricultura.exceptions import SafraNotFoundError


@pytest.mark.asyncio
async def test_safra_service_fluxo_criar_iniciar_colher():
    propriedade_service = PropriedadeService()
    producao_service = ProducaoService()
    safra_service = SafraService(
        propriedade_service=propriedade_service, producao_service=producao_service
    )
    prop = await propriedade_service.cadastrar(
        produtor_id=uuid4(),
        nome="Fazenda Sul",
        tipo=TipoPropriedade.PROPRIO,
        area_total_ha=80,
        area_cultivavel_ha=60,
    )
    cult = await producao_service.cadastrar_cultura(
        nome="Mandioca", tipo=TipoCultura.PERENE, ciclo_dias=300, produtividade_estimada_ton_ha=12.0
    )
    safra = await safra_service.criar_safra(
        codigo_propriedade=prop.codigo_propriedade,
        codigo_cultura=cult.codigo_cultura,
        ano=2026,
        area_plantada_ha=40,
        producao_estimada_ton=300,
    )
    assert safra.status == StatusSafra.PLANEJADA
    safra = await safra_service.iniciar(safra.codigo_safra)
    assert safra.status == StatusSafra.EM_ANDAMENTO
    safra = await safra_service.colher(safra.codigo_safra, 280)
    assert safra.status == StatusSafra.COLHIDA


def test_endpoint_criar_safra_retorna_201():
    mock_item = SimpleNamespace(
        id=uuid4(),
        codigo_safra="SAF/2026/000001",
        propriedade_id=uuid4(),
        cultura_id=uuid4(),
        ano=2026,
        area_plantada_ha=40,
        producao_estimada_ton=300,
        status="planejada",
        data_inicio=None,
        data_colheita=None,
        producao_real_ton=None,
    )
    service = SimpleNamespace(criar_safra=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(safras_router, prefix="/agricultura")
    app.dependency_overrides[get_safra_service] = lambda: service
    client = TestClient(app)
    response = client.post(
        "/agricultura/safras/",
        json={
            "codigo_propriedade": "PROP/2026/000001",
            "codigo_cultura": "CULT/2026/000001",
            "ano": 2026,
            "area_plantada_ha": 40,
            "producao_estimada_ton": 300,
        },
    )
    assert response.status_code == 201
    assert response.json()["codigo_safra"] == "SAF/2026/000001"


def test_endpoint_obter_safra_retorna_404():
    service = SimpleNamespace(
        obter=AsyncMock(side_effect=SafraNotFoundError("Safra nao encontrada"))
    )
    app = FastAPI()
    app.include_router(safras_router, prefix="/agricultura")
    app.dependency_overrides[get_safra_service] = lambda: service
    client = TestClient(app)
    response = client.get("/agricultura/safras/SAF/2026/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Safra nao encontrada"
