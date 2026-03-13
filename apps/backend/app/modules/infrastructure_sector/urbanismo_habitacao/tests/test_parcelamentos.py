from __future__ import annotations
from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.deps import get_parcelamento_service
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.endpoints.parcelamentos import router as parcelamentos_router
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.services.parcelamento_service import ParcelamentoService
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusParcelamento, TipoParcelamento
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.exceptions import ParcelamentoNotFoundError
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.repositories import SQLAlchemyParcelamentoRepository

@pytest.mark.asyncio
async def test_parcelamento_service_fluxo_sucesso():
    service = ParcelamentoService(parcelamento_repo=SQLAlchemyParcelamentoRepository())
    item = await service.criar(nome='Parcelamento ZRU Sul', tipo=TipoParcelamento.LOTEAMENTO, plano_diretor_id=uuid4(), zoneamento_id=uuid4(), provincia='Luanda', area_total=Decimal('250000.00'), quantidade_unidades_prevista=220, municipio='Luanda')
    assert item.status == StatusParcelamento.ELABORACAO
    assert item.codigo_parcelamento.startswith('PAR/')
    item = await service.iniciar_analise(item.codigo_parcelamento)
    assert item.status == StatusParcelamento.EM_ANALISE
    item = await service.aprovar(item.codigo_parcelamento)
    assert item.status == StatusParcelamento.APROVADO
    item = await service.iniciar_execucao(item.codigo_parcelamento)
    assert item.status == StatusParcelamento.EM_EXECUCAO
    item = await service.concluir(item.codigo_parcelamento, quantidade_unidades_resultante=215)
    assert item.status == StatusParcelamento.CONCLUIDO
    assert item.quantidade_unidades_resultante == 215

def test_endpoint_criar_parcelamento_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), codigo_parcelamento='PAR/2026/000001', nome='Parcelamento ZRU Sul', tipo=TipoParcelamento.LOTEAMENTO, status=StatusParcelamento.ELABORACAO, plano_diretor_id=uuid4(), zoneamento_id=uuid4(), provincia='Luanda', area_total=Decimal('250000.00'), quantidade_unidades_prevista=220, municipio='Luanda', area_publica_prevista=None, area_sistema_viario_prevista=None, quantidade_unidades_resultante=None, data_cadastro=date(2026, 3, 1), data_atualizacao=None, observacoes=None)
    service = SimpleNamespace(criar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(parcelamentos_router, prefix='/urbanismo-habitacao')
    app.dependency_overrides[get_parcelamento_service] = lambda: service
    client = TestClient(app)
    response = client.post('/urbanismo-habitacao/parcelamentos/', json={'nome': 'Parcelamento ZRU Sul', 'tipo': 'loteamento', 'plano_diretor_id': str(uuid4()), 'zoneamento_id': str(uuid4()), 'provincia': 'Luanda', 'area_total': '250000.00', 'quantidade_unidades_prevista': 220, 'municipio': 'Luanda'})
    assert response.status_code == 201
    assert response.json()['codigo_parcelamento'] == 'PAR/2026/000001'

def test_endpoint_obter_parcelamento_retorna_404():
    service = SimpleNamespace(obter_por_codigo=AsyncMock(side_effect=ParcelamentoNotFoundError('Parcelamento nao encontrado')))
    app = FastAPI()
    app.include_router(parcelamentos_router, prefix='/urbanismo-habitacao')
    app.dependency_overrides[get_parcelamento_service] = lambda: service
    client = TestClient(app)
    response = client.get('/urbanismo-habitacao/parcelamentos/PAR/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Parcelamento nao encontrado'