from __future__ import annotations
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.resources.agricultura.api.deps import get_propriedade_service
from app.modules.resources.agricultura.api.endpoints.propriedades import router as propriedades_router
from app.modules.resources.agricultura.application.services.propriedade_service import PropriedadeService
from app.modules.resources.agricultura.domain.enums import TipoPropriedade
from app.modules.resources.agricultura.exceptions import PropriedadeNotFoundError

@pytest.mark.asyncio
async def test_propriedade_service_cadastro_sucesso():
    service = PropriedadeService()
    item = await service.cadastrar(produtor_id=uuid4(), nome='Fazenda Kwanza', tipo=TipoPropriedade.PROPRIO, area_total_ha=120.0, area_cultivavel_ha=95.5)
    assert item.codigo_propriedade.startswith('PROP/')

def test_endpoint_cadastrar_propriedade_retorna_201():
    produtor_id = uuid4()
    mock_item = SimpleNamespace(id=uuid4(), codigo_propriedade='PROP/2026/000001', produtor_id=produtor_id, nome='Fazenda Kwanza', tipo=TipoPropriedade.PROPRIO, area_total_ha=120.0, area_cultivavel_ha=95.5, provincia='Luanda', municipio='Belas', data_cadastro='2026-02-28', ativo=True)
    service = SimpleNamespace(cadastrar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(propriedades_router, prefix='/agricultura')
    app.dependency_overrides[get_propriedade_service] = lambda: service
    client = TestClient(app)
    response = client.post('/agricultura/propriedades/', json={'produtor_id': str(produtor_id), 'nome': 'Fazenda Kwanza', 'tipo': 'proprio', 'area_total_ha': 120.0, 'area_cultivavel_ha': 95.5, 'provincia': 'Luanda', 'municipio': 'Belas'})
    assert response.status_code == 201
    assert response.json()['codigo_propriedade'] == 'PROP/2026/000001'

def test_endpoint_obter_propriedade_retorna_404():
    service = SimpleNamespace(obter=AsyncMock(side_effect=PropriedadeNotFoundError('Propriedade nao encontrada')))
    app = FastAPI()
    app.include_router(propriedades_router, prefix='/agricultura')
    app.dependency_overrides[get_propriedade_service] = lambda: service
    client = TestClient(app)
    response = client.get('/agricultura/propriedades/PROP/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Propriedade nao encontrada'