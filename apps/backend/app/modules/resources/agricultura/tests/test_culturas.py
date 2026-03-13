from __future__ import annotations
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.resources.agricultura.api.deps import get_producao_service
from app.modules.resources.agricultura.api.endpoints.culturas import router as culturas_router
from app.modules.resources.agricultura.application.services.producao_service import ProducaoService
from app.modules.resources.agricultura.domain.enums import TipoCultura
from app.modules.resources.agricultura.exceptions import CulturaNotFoundError

@pytest.mark.asyncio
async def test_producao_service_cadastra_cultura():
    service = ProducaoService()
    item = await service.cadastrar_cultura(nome='Milho', tipo=TipoCultura.GRAOS, ciclo_dias=120, produtividade_estimada_ton_ha=6.2)
    assert item.codigo_cultura.startswith('CULT/')

def test_endpoint_cadastrar_cultura_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), codigo_cultura='CULT/2026/000001', nome='Milho', tipo=TipoCultura.GRAOS, ciclo_dias=120, produtividade_estimada_ton_ha=6.2, data_registro='2026-02-28', ativa=True)
    service = SimpleNamespace(cadastrar_cultura=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(culturas_router, prefix='/agricultura')
    app.dependency_overrides[get_producao_service] = lambda: service
    client = TestClient(app)
    response = client.post('/agricultura/culturas/', json={'nome': 'Milho', 'tipo': 'graos', 'ciclo_dias': 120, 'produtividade_estimada_ton_ha': 6.2})
    assert response.status_code == 201
    assert response.json()['codigo_cultura'] == 'CULT/2026/000001'

def test_endpoint_obter_cultura_retorna_404():
    service = SimpleNamespace(obter_cultura=AsyncMock(side_effect=CulturaNotFoundError('Cultura nao encontrada')))
    app = FastAPI()
    app.include_router(culturas_router, prefix='/agricultura')
    app.dependency_overrides[get_producao_service] = lambda: service
    client = TestClient(app)
    response = client.get('/agricultura/culturas/CULT/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Cultura nao encontrada'