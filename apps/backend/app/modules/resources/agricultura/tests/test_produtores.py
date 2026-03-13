from __future__ import annotations
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.resources.agricultura.api.deps import get_produtor_service
from apps.backend.app.modules.resources.agricultura.api.endpoints.produtores import router as produtores_router
from apps.backend.app.modules.resources.agricultura.application.services.produtor_service import ProdutorService
from apps.backend.app.modules.resources.agricultura.domain.enums import StatusProdutor, TipoProdutor
from apps.backend.app.modules.resources.agricultura.domain.models.produtor import Produtor
from apps.backend.app.modules.resources.agricultura.exceptions import CitizenInactiveError, ProdutorAlreadyExistsError

@pytest.mark.asyncio
async def test_cadastrar_produtor_sucesso():
    citizen_id = uuid4()
    repo = SimpleNamespace(get_by_documento=AsyncMock(return_value=None), next_cadastro=AsyncMock(return_value='AGR/2026/000001'), save=AsyncMock(side_effect=lambda item: item))
    citizen = SimpleNamespace(is_citizen_active=AsyncMock(return_value=True))
    request = SimpleNamespace(create_request=AsyncMock(return_value=uuid4()), complete_request=AsyncMock(return_value=True))
    service = ProdutorService(repo, citizen, request)
    result = await service.cadastrar_produtor(nome='Joao Silva', documento='123456789LA', documento_tipo='BI', tipo=TipoProdutor.FAMILIAR, citizen_id=citizen_id)
    assert result.cadastro_produtor == 'AGR/2026/000001'
    assert result.status == StatusProdutor.PENDENTE
    request.create_request.assert_awaited_once()

@pytest.mark.asyncio
async def test_cadastrar_produtor_documento_duplicado():
    existente = Produtor.criar(nome='Maria', documento='DUP', documento_tipo='BI', tipo=TipoProdutor.PEQUENO)
    existente.status = StatusProdutor.ATIVO
    repo = SimpleNamespace(get_by_documento=AsyncMock(return_value=existente), next_cadastro=AsyncMock(), save=AsyncMock())
    service = ProdutorService(repo)
    with pytest.raises(ProdutorAlreadyExistsError):
        await service.cadastrar_produtor(nome='Outra', documento='DUP', documento_tipo='BI', tipo=TipoProdutor.PEQUENO)

@pytest.mark.asyncio
async def test_cadastrar_produtor_cidadao_inativo():
    repo = SimpleNamespace(get_by_documento=AsyncMock(return_value=None), next_cadastro=AsyncMock(return_value='AGR/2026/000010'), save=AsyncMock())
    citizen = SimpleNamespace(is_citizen_active=AsyncMock(return_value=False))
    service = ProdutorService(repo, citizen_service=citizen)
    with pytest.raises(CitizenInactiveError):
        await service.cadastrar_produtor(nome='Inativo', documento='999', documento_tipo='BI', tipo=TipoProdutor.MEDIO, citizen_id=uuid4())

def _client(service) -> TestClient:
    app = FastAPI()
    app.include_router(produtores_router, prefix='/agricultura')
    app.dependency_overrides[get_produtor_service] = lambda: service
    return TestClient(app)

def test_endpoint_cadastrar_produtor_retorna_201():
    produtor = Produtor.criar(nome='Carlos', documento='456', documento_tipo='BI', tipo=TipoProdutor.COOPERATIVA, citizen_id=uuid4())
    produtor.cadastro_produtor = 'AGR/2026/000077'
    produtor.data_cadastro = date(2026, 2, 1)
    service = SimpleNamespace(cadastrar_produtor=AsyncMock(return_value=produtor))
    client = _client(service)
    response = client.post('/agricultura/produtores/', json={'nome': 'Carlos', 'documento': '456', 'documento_tipo': 'BI', 'tipo': 'cooperativa', 'citizen_id': str(produtor.citizen_id)})
    assert response.status_code == 201
    assert response.json()['cadastro_produtor'] == 'AGR/2026/000077'

def test_endpoint_obter_produtor_retorna_404():
    service = SimpleNamespace(obter_por_cadastro=AsyncMock(return_value=None))
    client = _client(service)
    response = client.get('/agricultura/produtores/AGR/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Produtor nao encontrado'