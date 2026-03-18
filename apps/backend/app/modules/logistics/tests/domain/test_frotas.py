from __future__ import annotations
from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.logistics.api.deps import get_frota_service
from apps.backend.app.modules.logistics.api.endpoints.frotas import router as frotas_router
from apps.backend.app.modules.logistics.application.services import FrotaService
from apps.backend.app.modules.logistics.domain.enums import StatusFrota, TipoTarifa
from apps.backend.app.modules.logistics.domain.exceptions import FrotaNotFoundError
from apps.backend.app.modules.logistics.infrastructure.repositories import SQLAlchemyFrotaRepository

@pytest.mark.asyncio
async def test_frota_service_fluxo_completo():
    workflow_adapter = SimpleNamespace(iniciar_fluxo=AsyncMock(return_value='WF-TRN-001'), registrar_evento=AsyncMock(return_value=None))
    service_requests_adapter = SimpleNamespace(abrir_solicitacao=AsyncMock(return_value='SRQ-TRN-001'))
    financas_adapter = SimpleNamespace(validar_tarifa=AsyncMock(return_value=True), registrar_despesa_manutencao=AsyncMock(return_value=True))
    seguranca_adapter = SimpleNamespace(validar_regularidade_veiculo=AsyncMock(return_value=True))
    service = FrotaService(frota_repo=SQLAlchemyFrotaRepository(), workflow_adapter=workflow_adapter, service_requests_adapter=service_requests_adapter, financas_adapter=financas_adapter, seguranca_publica_adapter=seguranca_adapter)
    frota = await service.criar_frota(nome='Frota Metropolitana Norte', operadora_id=uuid4(), municipio='Luanda', provincia='Luanda')
    assert frota.status == StatusFrota.ATIVA
    assert frota.codigo_frota.startswith('FRT/')
    frota = await service.adicionar_veiculo(frota.codigo_frota, veiculo_id=uuid4(), placa='LD-45-67-AB', tipo='onibus', capacidade=80)
    assert len(frota.veiculos) == 1
    frota = await service.registrar_manutencao(frota.codigo_frota, veiculo_id=uuid4(), tipo='preventiva', oficina='Oficina Central', custo=Decimal('120000.00'), data_manutencao=date.today())
    assert len(frota.manutencoes) == 1
    frota = await service.atualizar_tarifa(frota.codigo_frota, tipo_tarifa=TipoTarifa.PUBLICA, valor=Decimal('250.00'), motivo='Recomposicao de custos operacionais')
    assert len(frota.tarifas) == 1
    frota = await service.registrar_fiscalizacao(frota.codigo_frota, fiscal_id=uuid4(), conformidade=True, apontamentos='Operacao regular')
    assert len(frota.fiscalizacoes) == 1
    assert len(frota.trilha_auditoria) >= 4
    workflow_adapter.iniciar_fluxo.assert_awaited_once()
    workflow_adapter.registrar_evento.assert_awaited()
    service_requests_adapter.abrir_solicitacao.assert_awaited_once()
    financas_adapter.validar_tarifa.assert_awaited_once()
    financas_adapter.registrar_despesa_manutencao.assert_awaited_once()
    seguranca_adapter.validar_regularidade_veiculo.assert_awaited_once()

def test_endpoint_criar_frota_retorna_201():
    item = SimpleNamespace(id=uuid4(), codigo_frota='FRT/2026/000001', nome='Frota Centro', operadora_id=uuid4(), municipio='Luanda', provincia='Luanda', status=StatusFrota.ATIVA, data_cadastro=date(2026, 3, 4), data_atualizacao=None, observacoes=None, veiculos=[], manutencoes=[], fiscalizacoes=[], tarifas=[], trilha_auditoria=[])
    service = SimpleNamespace(criar_frota=AsyncMock(return_value=item))
    service.has_workflow_adapter = lambda: True
    service.has_service_requests_adapter = lambda: True
    app = FastAPI()
    app.include_router(frotas_router, prefix='/transportes-logistica')
    app.dependency_overrides[get_frota_service] = lambda: service
    client = TestClient(app)
    response = client.post('/transportes-logistica/frotas/', json={'nome': 'Frota Centro', 'operadora_id': str(uuid4()), 'municipio': 'Luanda', 'provincia': 'Luanda'})
    assert response.status_code == 201
    assert response.json()['codigo_frota'] == 'FRT/2026/000001'

def test_endpoint_criar_frota_sem_workflow_retorna_503():
    service = SimpleNamespace(criar_frota=AsyncMock())
    service.has_workflow_adapter = lambda: False
    service.has_service_requests_adapter = lambda: True
    app = FastAPI()
    app.include_router(frotas_router, prefix='/transportes-logistica')
    app.dependency_overrides[get_frota_service] = lambda: service
    client = TestClient(app)
    response = client.post('/transportes-logistica/frotas/', json={'nome': 'Frota Centro', 'operadora_id': str(uuid4()), 'municipio': 'Luanda', 'provincia': 'Luanda'})
    assert response.status_code == 503
    assert 'Workflow indisponivel' in response.json()['detail']
    service.criar_frota.assert_not_awaited()

def test_endpoint_obter_frota_retorna_404():
    service = SimpleNamespace(obter_por_codigo=AsyncMock(side_effect=FrotaNotFoundError('Frota nao encontrada')))
    app = FastAPI()
    app.include_router(frotas_router, prefix='/transportes-logistica')
    app.dependency_overrides[get_frota_service] = lambda: service
    client = TestClient(app)
    response = client.get('/transportes-logistica/frotas/FRT/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Frota nao encontrada'