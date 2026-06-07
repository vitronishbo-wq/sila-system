from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.backend.app.modules.resources.pecuaria.api.deps import get_rebanho_service
from apps.backend.app.modules.resources.pecuaria.api.endpoints.rebanhos import (
    router as rebanhos_router,
)
from apps.backend.app.modules.resources.pecuaria.application.services.rebanho_service import (
    RebanhoService,
)
from apps.backend.app.modules.resources.pecuaria.domain.enums import TipoAnimal
from apps.backend.app.modules.resources.pecuaria.domain.models.rebanho import Rebanho


@pytest.mark.asyncio
async def test_rebanho_service_cadastro_sucesso():
    repository = SimpleNamespace(
        next_codigo=AsyncMock(return_value="REB/2026/000001"),
        save=AsyncMock(side_effect=lambda item: item),
        get_by_codigo=AsyncMock(),
        list_by_propriedade=AsyncMock(),
    )
    service = RebanhoService(repository=repository)
    item = await service.cadastrar(
        propriedade_id=uuid4(),
        tipo_animal=TipoAnimal.BOVINO,
        descricao="Matrizes leiteiras",
        quantidade_animais=10,
    )
    assert item.codigo_rebanho.startswith("REB/")


def test_endpoint_cadastrar_rebanho_retorna_201():
    mock_item = Rebanho.criar(
        propriedade_id=uuid4(),
        tipo_animal=TipoAnimal.BOVINO,
        descricao="Matrizes leiteiras",
        quantidade_animais=10,
    )
    mock_item.codigo_rebanho = "REB/2026/000001"
    service = SimpleNamespace(cadastrar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(rebanhos_router, prefix="/pecuaria")
    app.dependency_overrides[get_rebanho_service] = lambda: service
    client = TestClient(app)
    response = client.post(
        "/pecuaria/rebanhos/",
        json={
            "propriedade_id": str(mock_item.propriedade_id),
            "tipo_animal": "bovino",
            "descricao": "Matrizes leiteiras",
            "quantidade_animais": 10,
        },
    )
    assert response.status_code == 201
    assert response.json()["codigo_rebanho"] == "REB/2026/000001"


def test_endpoint_obter_rebanho_retorna_404():
    service = SimpleNamespace(obter=AsyncMock(side_effect=ValueError("Rebanho nao encontrado")))
    app = FastAPI()
    app.include_router(rebanhos_router, prefix="/pecuaria")
    app.dependency_overrides[get_rebanho_service] = lambda: service
    client = TestClient(app)
    response = client.get("/pecuaria/rebanhos/REB/2026/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Rebanho nao encontrado"
