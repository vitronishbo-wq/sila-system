from __future__ import annotations
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.resources.agricultura.api.deps import get_insumo_service
from apps.backend.app.modules.resources.agricultura.api.endpoints.insumos import router as insumos_router
from apps.backend.app.modules.resources.agricultura.application.services.insumo_service import InsumoService
from apps.backend.app.modules.resources.agricultura.domain.enums import TipoInsumo
from apps.backend.app.modules.resources.agricultura.exceptions import InsumoNotFoundError

@pytest.mark.asyncio
async def test_insumo_service_fluxo_entrada_baixa():
    service = InsumoService()
    item = await service.cadastrar(nome='Ureia', tipo=TipoInsumo.FERTILIZANTE, unidade_medida='kg', quantidade_inicial=100, custo_unitario=20)
    await service.registrar_entrada(item.codigo_insumo, 50)
    atualizado = await service.registrar_baixa(item.codigo_insumo, 30)
    assert atualizado.quantidade_estoque == 120

def test_endpoint_cadastrar_insumo_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), codigo_insumo='INS/2026/000001', nome='Ureia', tipo=TipoInsumo.FERTILIZANTE, unidade_medida='kg', quantidade_estoque=100, custo_unitario=20, data_registro='2026-02-28', ativo=True)
    service = SimpleNamespace(cadastrar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(insumos_router, prefix='/agricultura')
    app.dependency_overrides[get_insumo_service] = lambda: service
    client = TestClient(app)
    response = client.post('/agricultura/insumos/', json={'nome': 'Ureia', 'tipo': 'fertilizante', 'unidade_medida': 'kg', 'quantidade_inicial': 100, 'custo_unitario': 20})
    assert response.status_code == 201
    assert response.json()['codigo_insumo'] == 'INS/2026/000001'

def test_endpoint_obter_insumo_retorna_404():
    service = SimpleNamespace(obter=AsyncMock(side_effect=InsumoNotFoundError('Insumo nao encontrado')))
    app = FastAPI()
    app.include_router(insumos_router, prefix='/agricultura')
    app.dependency_overrides[get_insumo_service] = lambda: service
    client = TestClient(app)
    response = client.get('/agricultura/insumos/INS/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Insumo nao encontrado'