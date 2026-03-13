from __future__ import annotations
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.resources.pescas.api.deps import get_pescador_service
from apps.backend.app.modules.resources.pescas.api.endpoints.pescadores import router as pescadores_router
from apps.backend.app.modules.resources.pescas.application.services.pescador_service import PescadorService
from apps.backend.app.modules.resources.pescas.domain.enums import TipoPescador

@pytest.mark.asyncio
async def test_cadastrar_pescador_sucesso():
    repo = SimpleNamespace(get_by_numero_registro=AsyncMock(return_value=None), next_registro=AsyncMock(return_value='PES/2026/000001'), save=AsyncMock(side_effect=lambda item: item))
    citizen = SimpleNamespace(is_citizen_active=AsyncMock(return_value=True))
    request = SimpleNamespace(create_request=AsyncMock(return_value=uuid4()))
    service = PescadorService(repo, citizen, request)
    item = await service.cadastrar_pescador(nome='Mario', tipo=TipoPescador.ARTESANAL, citizen_id=uuid4())
    assert item.numero_registro == 'PES/2026/000001'

def test_endpoint_obter_pescador_404():
    service = SimpleNamespace(buscar_pescador=AsyncMock(side_effect=ValueError('Pescador nao encontrado')))
    app = FastAPI()
    app.include_router(pescadores_router, prefix='/pescas')
    app.dependency_overrides[get_pescador_service] = lambda: service
    client = TestClient(app)
    response = client.get(f'/pescas/pescadores/{uuid4()}')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Pescador nao encontrado'