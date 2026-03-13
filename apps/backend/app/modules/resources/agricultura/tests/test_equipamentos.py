from __future__ import annotations
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.resources.agricultura.api.deps import get_equipamento_service
from apps.backend.app.modules.resources.agricultura.api.endpoints.equipamentos import router as equipamentos_router
from apps.backend.app.modules.resources.agricultura.application.services.equipamento_service import EquipamentoService
from apps.backend.app.modules.resources.agricultura.domain.enums import StatusEquipamento, TipoEquipamento
from apps.backend.app.modules.resources.agricultura.exceptions import EquipamentoNotFoundError

@pytest.mark.asyncio
async def test_equipamento_service_fluxo_uso():
    service = EquipamentoService()
    equipamento = await service.cadastrar(nome='Trator XP', tipo=TipoEquipamento.TRATOR, ano_fabricacao=2024)
    assert equipamento.status == StatusEquipamento.DISPONIVEL
    equipamento = await service.iniciar_uso(equipamento.codigo_equipamento)
    equipamento = await service.registrar_uso(equipamento.codigo_equipamento, horas=2.5)
    equipamento = await service.finalizar_uso(equipamento.codigo_equipamento)
    assert equipamento.status == StatusEquipamento.DISPONIVEL
    assert equipamento.horas_uso == 2.5

def test_endpoint_cadastrar_equipamento_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), codigo_equipamento='EQP/2026/000001', nome='Trator XP', tipo='trator', fabricante='AgroTech', modelo='XP-90', ano_fabricacao=2024, data_aquisicao=None, status='disponivel', horas_uso=0.0, ultima_manutencao=None)
    service = SimpleNamespace(cadastrar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(equipamentos_router, prefix='/agricultura')
    app.dependency_overrides[get_equipamento_service] = lambda: service
    client = TestClient(app)
    response = client.post('/agricultura/equipamentos/', json={'nome': 'Trator XP', 'tipo': 'trator', 'fabricante': 'AgroTech', 'modelo': 'XP-90', 'ano_fabricacao': 2024})
    assert response.status_code == 201
    assert response.json()['codigo_equipamento'] == 'EQP/2026/000001'

def test_endpoint_obter_equipamento_retorna_404():
    service = SimpleNamespace(obter=AsyncMock(side_effect=EquipamentoNotFoundError('Equipamento nao encontrado')))
    app = FastAPI()
    app.include_router(equipamentos_router, prefix='/agricultura')
    app.dependency_overrides[get_equipamento_service] = lambda: service
    client = TestClient(app)
    response = client.get('/agricultura/equipamentos/EQP/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Equipamento nao encontrado'