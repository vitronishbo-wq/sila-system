from __future__ import annotations
from datetime import date, timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.infrastructure.api.deps import get_edital_service
from apps.backend.app.modules.infrastructure.api.endpoints.editais import router as editais_router
from apps.backend.app.modules.infrastructure.application.services.edital_service import EditalService
from apps.backend.app.modules.infrastructure.domain.enums import StatusEdital
from apps.backend.app.modules.infrastructure.domain.exceptions import EditalNotFoundError
from apps.backend.app.modules.infrastructure.infrastructure.repositories import SQLAlchemyEditalRepository

@pytest.mark.asyncio
async def test_edital_service_fluxo_sucesso():
    service = EditalService(edital_repo=SQLAlchemyEditalRepository())
    data_publicacao = date.today()
    data_abertura = data_publicacao + timedelta(days=5)
    data_encerramento = data_publicacao + timedelta(days=20)
    item = await service.publicar(titulo='Edital de Pavimentacao 2026', objeto='Contratacao para pavimentacao de vias urbanas', licitacao_id=uuid4(), data_publicacao=data_publicacao, data_abertura=data_abertura, data_encerramento=data_encerramento)
    assert item.status == StatusEdital.PUBLICADO
    assert item.numero_edital.startswith('EDT/')
    assert item.versao == 1
    item = await service.impugnar(item.numero_edital, motivo='Questionamento tecnico')
    assert item.status == StatusEdital.IMPUGNADO
    item = await service.retificar(item.numero_edital, descricao='Ajuste de especificacao')
    assert item.status == StatusEdital.RETIFICADO
    assert item.versao == 2
    item = await service.encerrar(item.numero_edital, data_encerramento=data_abertura + timedelta(days=10))
    assert item.status == StatusEdital.ENCERRADO
    assert item.data_encerramento == data_abertura + timedelta(days=10)

def test_endpoint_publicar_edital_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), numero_edital='EDT/2026/000001', titulo='Edital de Pavimentacao 2026', objeto='Contratacao para pavimentacao de vias urbanas', licitacao_id=uuid4(), status=StatusEdital.PUBLICADO, data_publicacao=date(2026, 3, 1), data_abertura=date(2026, 3, 6), data_encerramento=date(2026, 3, 21), data_cadastro=date(2026, 3, 1), versao=1, data_atualizacao=None, observacoes=None)
    service = SimpleNamespace(publicar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(editais_router, prefix='/obras-publicas')
    app.dependency_overrides[get_edital_service] = lambda: service
    client = TestClient(app)
    response = client.post('/obras-publicas/editais/', json={'titulo': 'Edital de Pavimentacao 2026', 'objeto': 'Contratacao para pavimentacao de vias urbanas', 'licitacao_id': str(uuid4()), 'data_publicacao': '2026-03-01', 'data_abertura': '2026-03-06', 'data_encerramento': '2026-03-21'})
    assert response.status_code == 201
    assert response.json()['numero_edital'] == 'EDT/2026/000001'

def test_endpoint_obter_edital_retorna_404():
    service = SimpleNamespace(obter_por_numero=AsyncMock(side_effect=EditalNotFoundError('Edital nao encontrado')))
    app = FastAPI()
    app.include_router(editais_router, prefix='/obras-publicas')
    app.dependency_overrides[get_edital_service] = lambda: service
    client = TestClient(app)
    response = client.get('/obras-publicas/editais/EDT/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Edital nao encontrado'
