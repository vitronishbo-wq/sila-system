from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.backend.app.modules.resources.pecuaria.api.deps import get_propriedade_service
from apps.backend.app.modules.resources.pecuaria.api.endpoints.propriedades import (
    router as propriedades_router,
)
from apps.backend.app.modules.resources.pecuaria.application.services.propriedade_service import (
    PropriedadeService,
)
from apps.backend.app.modules.resources.pecuaria.domain.models.propriedade_pecuaria import (
    PropriedadePecuaria,
)


@pytest.mark.asyncio
async def test_propriedade_service_cadastro_sucesso():
    repository = SimpleNamespace(
        next_codigo=AsyncMock(return_value="PROP/2026/000001"),
        save=AsyncMock(side_effect=lambda item: item),
        get_by_codigo=AsyncMock(),
        list_by_pecuarista=AsyncMock(),
    )
    service = PropriedadeService(repository=repository)
    item = await service.cadastrar(
        pecuarista_id=uuid4(),
        nome="Fazenda Boa Vista",
        area_total_ha=120.0,
        municipio="Belas",
        provincia="Luanda",
    )
    assert item.codigo_propriedade.startswith("PROP/")


def test_endpoint_cadastrar_propriedade_retorna_201():
    pecuarista_id = uuid4()
    mock_item = PropriedadePecuaria.criar(
        pecuarista_id=pecuarista_id,
        nome="Fazenda Boa Vista",
        area_total_ha=120.0,
        municipio="Belas",
        provincia="Luanda",
    )
    mock_item.codigo_propriedade = "PROP/2026/000001"
    service = SimpleNamespace(cadastrar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(propriedades_router, prefix="/pecuaria")
    app.dependency_overrides[get_propriedade_service] = lambda: service
    client = TestClient(app)
    response = client.post(
        "/pecuaria/propriedades/",
        json={
            "pecuarista_id": str(pecuarista_id),
            "nome": "Fazenda Boa Vista",
            "area_total_ha": 120.0,
            "municipio": "Belas",
            "provincia": "Luanda",
        },
    )
    assert response.status_code == 201
    assert response.json()["codigo_propriedade"] == "PROP/2026/000001"


def test_endpoint_obter_propriedade_retorna_404():
    service = SimpleNamespace(
        obter=AsyncMock(side_effect=ValueError("Propriedade pecuaria nao encontrada"))
    )
    app = FastAPI()
    app.include_router(propriedades_router, prefix="/pecuaria")
    app.dependency_overrides[get_propriedade_service] = lambda: service
    client = TestClient(app)
    response = client.get("/pecuaria/propriedades/PROP/2026/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Propriedade pecuaria nao encontrada"
