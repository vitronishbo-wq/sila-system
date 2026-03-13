from __future__ import annotations
from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.deps import get_zoneamento_service
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.endpoints.zoneamento import router as zoneamento_router
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.services.zoneamento_service import ZoneamentoService
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusZoneamento, TipoZona, UsoPermitido
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.exceptions import ZoneamentoNotFoundError
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.repositories import SQLAlchemyZoneamentoRepository

@pytest.mark.asyncio
async def test_zoneamento_service_fluxo_sucesso():
    service = ZoneamentoService(zoneamento_repo=SQLAlchemyZoneamentoRepository())
    item = await service.criar(nome='Zona Residencial Central', tipo_zona=TipoZona.RESIDENCIAL, plano_diretor_id=uuid4(), provincia='Luanda', usos_permitidos=[UsoPermitido.HABITACIONAL, UsoPermitido.SERVICOS], municipio='Luanda')
    assert item.status == StatusZoneamento.ELABORACAO
    assert item.codigo_zoneamento.startswith('ZON/')
    item = await service.iniciar_consulta_publica(item.codigo_zoneamento)
    assert item.status == StatusZoneamento.EM_CONSULTA
    item = await service.aprovar(item.codigo_zoneamento)
    assert item.status == StatusZoneamento.APROVADO
    item = await service.vigorar(item.codigo_zoneamento, data_inicio_vigencia=date.today())
    assert item.status == StatusZoneamento.VIGENTE
    item = await service.atualizar_parametros(item.codigo_zoneamento, coeficiente_aproveitamento_max=Decimal('2.50'), taxa_ocupacao_max=Decimal('0.70'), gabarito_maximo=18)
    assert item.coeficiente_aproveitamento_max == Decimal('2.50')
    assert item.gabarito_maximo == 18
    item = await service.suspender(item.codigo_zoneamento, motivo='Revisao tecnica')
    assert item.status == StatusZoneamento.SUSPENSO
    item = await service.revogar(item.codigo_zoneamento, motivo='Substituicao normativa')
    assert item.status == StatusZoneamento.REVOGADO

def test_endpoint_criar_zoneamento_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), codigo_zoneamento='ZON/2026/000001', nome='Zona Residencial Central', tipo_zona=TipoZona.RESIDENCIAL, status=StatusZoneamento.ELABORACAO, plano_diretor_id=uuid4(), provincia='Luanda', usos_permitidos=[UsoPermitido.HABITACIONAL, UsoPermitido.SERVICOS], municipio='Luanda', coeficiente_aproveitamento_max=None, taxa_ocupacao_max=None, gabarito_maximo=None, recuo_frontal_minimo=None, permeabilidade_minima=None, area_lote_minima=None, data_inicio_vigencia=None, data_cadastro=date(2026, 3, 1), data_atualizacao=None, observacoes=None)
    service = SimpleNamespace(criar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(zoneamento_router, prefix='/urbanismo-habitacao')
    app.dependency_overrides[get_zoneamento_service] = lambda: service
    client = TestClient(app)
    response = client.post('/urbanismo-habitacao/zoneamento/', json={'nome': 'Zona Residencial Central', 'tipo_zona': 'residencial', 'plano_diretor_id': str(uuid4()), 'provincia': 'Luanda', 'usos_permitidos': ['habitacional', 'servicos'], 'municipio': 'Luanda'})
    assert response.status_code == 201
    assert response.json()['codigo_zoneamento'] == 'ZON/2026/000001'

def test_endpoint_obter_zoneamento_retorna_404():
    service = SimpleNamespace(obter_por_codigo=AsyncMock(side_effect=ZoneamentoNotFoundError('Zoneamento nao encontrado')))
    app = FastAPI()
    app.include_router(zoneamento_router, prefix='/urbanismo-habitacao')
    app.dependency_overrides[get_zoneamento_service] = lambda: service
    client = TestClient(app)
    response = client.get('/urbanismo-habitacao/zoneamento/ZON/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Zoneamento nao encontrado'