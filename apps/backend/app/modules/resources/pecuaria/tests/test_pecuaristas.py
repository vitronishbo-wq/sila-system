from __future__ import annotations
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.resources.pecuaria.api.deps import get_pecuarista_service
from apps.backend.app.modules.resources.pecuaria.api.endpoints.pecuaristas import router as pecuaristas_router
from apps.backend.app.modules.resources.pecuaria.application.services.pecuarista_service import PecuaristaService
from apps.backend.app.modules.resources.pecuaria.domain.enums import StatusPecuarista
from apps.backend.app.modules.resources.pecuaria.domain.models.pecuarista import Pecuarista

@pytest.mark.asyncio
async def test_cadastrar_pecuarista_sucesso():
    citizen_id = uuid4()
    repo = SimpleNamespace(get_by_documento=AsyncMock(return_value=None), next_cadastro=AsyncMock(return_value='PEC/2026/000001'), save=AsyncMock(side_effect=lambda item: item))
    citizen = SimpleNamespace(is_citizen_active=AsyncMock(return_value=True))
    request = SimpleNamespace(create_request=AsyncMock(return_value=uuid4()), complete_request=AsyncMock(return_value=True))
    service = PecuaristaService(repo, citizen, request)
    result = await service.cadastrar_pecuarista(nome='Ana', documento='123456789', documento_tipo='BI', citizen_id=citizen_id)
    assert result.cadastro_pecuarista == 'PEC/2026/000001'
    assert result.status == StatusPecuarista.PENDENTE
    request.create_request.assert_awaited_once()

def _client(service) -> TestClient:
    app = FastAPI()
    app.include_router(pecuaristas_router, prefix='/pecuaria')
    app.dependency_overrides[get_pecuarista_service] = lambda: service
    return TestClient(app)

def test_endpoint_cadastrar_pecuarista_retorna_201():
    item = Pecuarista.criar(nome='Carlos', documento='456', documento_tipo='BI', citizen_id=uuid4())
    item.cadastro_pecuarista = 'PEC/2026/000077'
    item.data_cadastro = date(2026, 2, 1)
    service = SimpleNamespace(cadastrar_pecuarista=AsyncMock(return_value=item))
    client = _client(service)
    response = client.post('/pecuaria/pecuaristas/', json={'nome': 'Carlos', 'documento': '456', 'documento_tipo': 'BI', 'citizen_id': str(item.citizen_id)})
    assert response.status_code == 201
    assert response.json()['cadastro_pecuarista'] == 'PEC/2026/000077'

def test_endpoint_obter_pecuarista_retorna_404():
    service = SimpleNamespace(obter_por_cadastro=AsyncMock(return_value=None))
    client = _client(service)
    response = client.get('/pecuaria/pecuaristas/PEC/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Pecuarista nao encontrado'