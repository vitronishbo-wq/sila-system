from __future__ import annotations
from datetime import date, timedelta
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.resources.aguas_saneamento.api.deps import get_outorga_service
from app.modules.resources.aguas_saneamento.api.endpoints.outorgas import router as outorgas_router
from app.modules.resources.aguas_saneamento.application.services.outorga_service import OutorgaService
from app.modules.resources.aguas_saneamento.domain.enums import StatusOutorga, TipoCaptacao, TipoOutorga, TipoUso
from app.modules.resources.aguas_saneamento.exceptions import OutorgaNotFoundError
from app.modules.resources.aguas_saneamento.infrastructure.repositories import SQLAlchemyOutorgaRepository

@pytest.mark.asyncio
async def test_outorga_service_fluxo_sucesso():
    service = OutorgaService(outorga_repo=SQLAlchemyOutorgaRepository())
    outorga = await service.requerer(tipo=TipoOutorga.CAPTACAO, requerente_id=uuid4(), requerente_tipo='citizen', corpo_hidrico_id=uuid4(), tipo_captacao=TipoCaptacao.SUPERFICIAL, vazao=Decimal('12.50'), unidade_vazao='m3/h', tempo_captacao=8, periodo_captacao='intermitente', finalidade_uso=TipoUso.IRRIGACAO)
    assert outorga.status == StatusOutorga.REQUERIDA
    outorga = await service.iniciar_analise(outorga.numero_outorga)
    assert outorga.status == StatusOutorga.EM_ANALISE
    outorga = await service.deferir(outorga.numero_outorga, data_validade_inicio=date.today(), data_validade_fim=date.today() + timedelta(days=365), data_publicacao=date.today(), processo='PROC-2026-001')
    assert outorga.status == StatusOutorga.DEFERIDA
    outorga = await service.renovar(outorga.numero_outorga, nova_data_fim=date.today() + timedelta(days=730))
    assert outorga.status == StatusOutorga.DEFERIDA

def test_endpoint_requerer_outorga_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), numero_outorga='OUT/2026/000001', tipo=TipoOutorga.CAPTACAO, status=StatusOutorga.REQUERIDA, requerente_id=uuid4(), requerente_tipo='citizen', corpo_hidrico_id=uuid4(), tipo_captacao=TipoCaptacao.SUPERFICIAL, vazao=Decimal('12.50'), unidade_vazao='m3/h', tempo_captacao=8, periodo_captacao='intermitente', finalidade_uso=TipoUso.IRRIGACAO, data_requerimento=date(2026, 3, 1), data_validade_inicio=None, data_validade_fim=None, data_publicacao=None, processo_administrativo=None, coordenadas_lat=None, coordenadas_long=None, observacoes=None)
    service = SimpleNamespace(requerer=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(outorgas_router, prefix='/aguas-saneamento')
    app.dependency_overrides[get_outorga_service] = lambda: service
    client = TestClient(app)
    response = client.post('/aguas-saneamento/outorgas/', json={'tipo': 'captacao', 'requerente_id': str(uuid4()), 'requerente_tipo': 'citizen', 'corpo_hidrico_id': str(uuid4()), 'tipo_captacao': 'superficial', 'vazao': '12.50', 'unidade_vazao': 'm3/h', 'tempo_captacao': 8, 'periodo_captacao': 'intermitente', 'finalidade_uso': 'irrigacao'})
    assert response.status_code == 201
    assert response.json()['numero_outorga'] == 'OUT/2026/000001'

def test_endpoint_obter_outorga_retorna_404():
    service = SimpleNamespace(obter_por_numero=AsyncMock(side_effect=OutorgaNotFoundError('Outorga nao encontrada')))
    app = FastAPI()
    app.include_router(outorgas_router, prefix='/aguas-saneamento')
    app.dependency_overrides[get_outorga_service] = lambda: service
    client = TestClient(app)
    response = client.get('/aguas-saneamento/outorgas/OUT/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Outorga nao encontrada'