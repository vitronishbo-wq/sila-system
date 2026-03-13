from __future__ import annotations
from datetime import date, timedelta
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.deps import get_loteamento_service
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.endpoints.loteamentos import router as loteamentos_router
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.services.loteamento_service import LoteamentoService
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusLoteamento, TipoLoteamento
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.exceptions import LoteamentoNotFoundError
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.repositories import SQLAlchemyLoteamentoRepository

@pytest.mark.asyncio
async def test_loteamento_service_fluxo_sucesso():
    service = LoteamentoService(loteamento_repo=SQLAlchemyLoteamentoRepository())
    item = await service.criar(nome='Loteamento Nova Centralidade', tipo=TipoLoteamento.ABERTO, parcelamento_id=uuid4(), plano_diretor_id=uuid4(), zoneamento_id=uuid4(), provincia='Luanda', area_total=Decimal('180000.00'), quantidade_lotes_prevista=300, municipio='Luanda')
    assert item.status == StatusLoteamento.PROPOSTO
    assert item.codigo_loteamento.startswith('LOT/')
    item = await service.aprovar(item.codigo_loteamento)
    assert item.status == StatusLoteamento.APROVADO
    item = await service.iniciar_implantacao(item.codigo_loteamento, data_inicio_real=date.today())
    assert item.status == StatusLoteamento.EM_IMPLANTACAO
    item = await service.registrar_implantacao(item.codigo_loteamento, quantidade_lotes_implantada=140)
    assert item.quantidade_lotes_implantada == 140
    item = await service.suspender(item.codigo_loteamento, motivo='Ajuste de drenagem')
    assert item.status == StatusLoteamento.SUSPENSO
    item = await service.retomar(item.codigo_loteamento)
    assert item.status == StatusLoteamento.EM_IMPLANTACAO
    item = await service.registrar_implantacao(item.codigo_loteamento, quantidade_lotes_implantada=300)
    item = await service.concluir(item.codigo_loteamento, data_fim_real=date.today() + timedelta(days=1))
    assert item.status == StatusLoteamento.CONCLUIDO

def test_endpoint_criar_loteamento_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), codigo_loteamento='LOT/2026/000001', nome='Loteamento Nova Centralidade', tipo=TipoLoteamento.ABERTO, status=StatusLoteamento.PROPOSTO, parcelamento_id=uuid4(), plano_diretor_id=uuid4(), zoneamento_id=uuid4(), provincia='Luanda', area_total=Decimal('180000.00'), quantidade_lotes_prevista=300, municipio='Luanda', quantidade_lotes_implantada=0, area_lotes=None, area_verde=None, area_institucional=None, data_inicio_prevista=None, data_fim_prevista=None, data_inicio_real=None, data_fim_real=None, data_cadastro=date(2026, 3, 1), data_atualizacao=None, observacoes=None)
    service = SimpleNamespace(criar=AsyncMock(return_value=mock_item))
    service.has_gestao_fundiaria_adapter = lambda: True
    service.has_financas_adapter = lambda: True
    service.has_workflow_adapter = lambda: True
    app = FastAPI()
    app.include_router(loteamentos_router, prefix='/urbanismo-habitacao')
    app.dependency_overrides[get_loteamento_service] = lambda: service
    client = TestClient(app)
    response = client.post('/urbanismo-habitacao/loteamentos/', json={'nome': 'Loteamento Nova Centralidade', 'tipo': 'aberto', 'parcelamento_id': str(uuid4()), 'plano_diretor_id': str(uuid4()), 'zoneamento_id': str(uuid4()), 'provincia': 'Luanda', 'area_total': '180000.00', 'quantidade_lotes_prevista': 300, 'municipio': 'Luanda'})
    assert response.status_code == 201
    assert response.json()['codigo_loteamento'] == 'LOT/2026/000001'

def test_endpoint_obter_loteamento_retorna_404():
    service = SimpleNamespace(obter_por_codigo=AsyncMock(side_effect=LoteamentoNotFoundError('Loteamento nao encontrado')))
    app = FastAPI()
    app.include_router(loteamentos_router, prefix='/urbanismo-habitacao')
    app.dependency_overrides[get_loteamento_service] = lambda: service
    client = TestClient(app)
    response = client.get('/urbanismo-habitacao/loteamentos/LOT/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Loteamento nao encontrado'

def test_endpoint_criar_loteamento_sem_adapter_critico_retorna_503():
    service = SimpleNamespace(criar=AsyncMock())
    service.has_gestao_fundiaria_adapter = lambda: False
    service.has_financas_adapter = lambda: True
    service.has_workflow_adapter = lambda: True
    app = FastAPI()
    app.include_router(loteamentos_router, prefix='/urbanismo-habitacao')
    app.dependency_overrides[get_loteamento_service] = lambda: service
    client = TestClient(app)
    response = client.post('/urbanismo-habitacao/loteamentos/', json={'nome': 'Loteamento Nova Centralidade', 'tipo': 'aberto', 'parcelamento_id': str(uuid4()), 'plano_diretor_id': str(uuid4()), 'zoneamento_id': str(uuid4()), 'provincia': 'Luanda', 'area_total': '180000.00', 'quantidade_lotes_prevista': 300})
    assert response.status_code == 503
    assert 'Gestao Fundiaria indisponivel' in response.json()['detail']
    service.criar.assert_not_awaited()