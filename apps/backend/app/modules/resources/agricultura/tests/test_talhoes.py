from __future__ import annotations
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.resources.agricultura.api.deps import get_talhao_service
from app.modules.resources.agricultura.api.endpoints.talhoes import router as talhoes_router
from app.modules.resources.agricultura.application.services.propriedade_service import PropriedadeService
from app.modules.resources.agricultura.application.services.talhao_service import TalhaoService
from app.modules.resources.agricultura.domain.enums import StatusTalhao, TipoPropriedade
from app.modules.resources.agricultura.exceptions import TalhaoNotFoundError

@pytest.mark.asyncio
async def test_talhao_service_cadastrar_desativar_ativar():
    propriedade_service = PropriedadeService()
    prop = await propriedade_service.cadastrar(produtor_id=uuid4(), nome='Fazenda Talhao', tipo=TipoPropriedade.PROPRIO, area_total_ha=50, area_cultivavel_ha=40)
    service = TalhaoService(propriedade_service=propriedade_service)
    talhao = await service.cadastrar(codigo_propriedade=prop.codigo_propriedade, nome='Talhao 1', area_ha=12, irrigado=True)
    assert talhao.status == StatusTalhao.ATIVO
    talhao = await service.desativar(talhao.codigo_talhao)
    assert talhao.status == StatusTalhao.INATIVO
    talhao = await service.ativar(talhao.codigo_talhao)
    assert talhao.status == StatusTalhao.ATIVO

def test_endpoint_cadastrar_talhao_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), codigo_talhao='TAL/2026/000001', codigo_propriedade='PROP/2026/000001', nome='Talhao 1', area_ha=12.0, tipo_solo='argiloso', irrigado=True, status='ativo', data_cadastro='2026-02-28')
    service = SimpleNamespace(cadastrar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(talhoes_router, prefix='/agricultura')
    app.dependency_overrides[get_talhao_service] = lambda: service
    client = TestClient(app)
    response = client.post('/agricultura/talhoes/', json={'codigo_propriedade': 'PROP/2026/000001', 'nome': 'Talhao 1', 'area_ha': 12, 'tipo_solo': 'argiloso', 'irrigado': True})
    assert response.status_code == 201
    assert response.json()['codigo_talhao'] == 'TAL/2026/000001'

def test_endpoint_obter_talhao_retorna_404():
    service = SimpleNamespace(obter=AsyncMock(side_effect=TalhaoNotFoundError('Talhao nao encontrado')))
    app = FastAPI()
    app.include_router(talhoes_router, prefix='/agricultura')
    app.dependency_overrides[get_talhao_service] = lambda: service
    client = TestClient(app)
    response = client.get('/agricultura/talhoes/TAL/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Talhao nao encontrado'