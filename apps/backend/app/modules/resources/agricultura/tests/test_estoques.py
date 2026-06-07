from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.backend.app.modules.resources.agricultura.api.deps import get_estoque_service
from apps.backend.app.modules.resources.agricultura.api.endpoints.estoques import (
    router as estoques_router,
)
from apps.backend.app.modules.resources.agricultura.application.services.estoque_service import (
    EstoqueService,
)
from apps.backend.app.modules.resources.agricultura.application.services.insumo_service import (
    InsumoService,
)
from apps.backend.app.modules.resources.agricultura.domain.enums import StatusEstoque, TipoInsumo
from apps.backend.app.modules.resources.agricultura.exceptions import EstoqueNotFoundError


@pytest.mark.asyncio
async def test_estoque_service_criar_e_listar_baixo():
    insumo_service = InsumoService()
    insumo = await insumo_service.cadastrar(
        nome="NPK",
        tipo=TipoInsumo.FERTILIZANTE,
        unidade_medida="kg",
        quantidade_inicial=50,
        custo_unitario=15,
    )
    service = EstoqueService(insumo_service=insumo_service)
    item = await service.criar_controle(codigo_insumo=insumo.codigo_insumo, quantidade_minima=60)
    assert item.status == StatusEstoque.BAIXO
    baixo = await service.listar(somente_baixo=True)
    assert len(baixo) == 1


def test_endpoint_criar_controle_estoque_retorna_201():
    mock_item = SimpleNamespace(
        id=uuid4(),
        codigo_estoque="EST/2026/000001",
        codigo_insumo="INS/2026/000001",
        quantidade_atual=40.0,
        quantidade_minima=60.0,
        status="baixo",
        data_atualizacao="2026-02-28T00:00:00",
    )
    service = SimpleNamespace(criar_controle=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(estoques_router, prefix="/agricultura")
    app.dependency_overrides[get_estoque_service] = lambda: service
    client = TestClient(app)
    response = client.post(
        "/agricultura/estoques/", json={"codigo_insumo": "INS/2026/000001", "quantidade_minima": 60}
    )
    assert response.status_code == 201
    assert response.json()["codigo_estoque"] == "EST/2026/000001"


def test_endpoint_obter_estoque_retorna_404():
    service = SimpleNamespace(
        obter=AsyncMock(side_effect=EstoqueNotFoundError("Controle de estoque nao encontrado"))
    )
    app = FastAPI()
    app.include_router(estoques_router, prefix="/agricultura")
    app.dependency_overrides[get_estoque_service] = lambda: service
    client = TestClient(app)
    response = client.get("/agricultura/estoques/EST/2026/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Controle de estoque nao encontrado"
