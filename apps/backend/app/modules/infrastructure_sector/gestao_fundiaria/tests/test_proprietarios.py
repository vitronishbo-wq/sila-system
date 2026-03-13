from __future__ import annotations
from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.infrastructure_sector.gestao_fundiaria.api.deps import get_proprietario_service
from app.modules.infrastructure_sector.gestao_fundiaria.api.endpoints.proprietarios import router as proprietarios_router
from app.modules.infrastructure_sector.gestao_fundiaria.application.services.proprietario_service import ProprietarioService
from app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import TipoPessoa, TipoTitularidade
from app.modules.infrastructure_sector.gestao_fundiaria.exceptions import ProprietarioNotFoundError
from app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.repositories import SQLAlchemyProprietarioRepository

@pytest.mark.asyncio
async def test_proprietario_service_fluxo_sucesso():
    service = ProprietarioService(proprietario_repo=SQLAlchemyProprietarioRepository())
    item = await service.cadastrar(nome='Joao Manuel', documento='BI1234567LA045', tipo_pessoa=TipoPessoa.SINGULAR, tipo_titularidade=TipoTitularidade.PROPRIETARIO, email='joao@example.gov.ao')
    assert item.numero_cadastro.startswith('PRP/')
    assert item.ativo is True
    item = await service.atualizar_titularidade(item.numero_cadastro, tipo_titularidade=TipoTitularidade.COTITULAR, percentual_titularidade=Decimal('50.00'))
    assert item.tipo_titularidade == TipoTitularidade.COTITULAR
    assert item.percentual_titularidade == Decimal('50.00')
    item = await service.atualizar_contato(item.numero_cadastro, telefone='+244923000111', endereco='Rua B, 20 - Luanda')
    assert item.telefone == '+244923000111'

def test_endpoint_cadastrar_proprietario_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), numero_cadastro='PRP/2026/000001', nome='Joao Manuel', documento='BI1234567LA045', tipo_pessoa=TipoPessoa.SINGULAR, tipo_titularidade=TipoTitularidade.PROPRIETARIO, data_cadastro=date(2026, 3, 1), ativo=True, percentual_titularidade=None, email='joao@example.gov.ao', telefone=None, endereco=None, data_atualizacao=None, observacoes=None)
    service = SimpleNamespace(cadastrar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(proprietarios_router, prefix='/gestao-fundiaria')
    app.dependency_overrides[get_proprietario_service] = lambda: service
    client = TestClient(app)
    response = client.post('/gestao-fundiaria/proprietarios/', json={'nome': 'Joao Manuel', 'documento': 'BI1234567LA045', 'tipo_pessoa': 'singular', 'tipo_titularidade': 'proprietario', 'email': 'joao@example.gov.ao'})
    assert response.status_code == 201
    assert response.json()['numero_cadastro'] == 'PRP/2026/000001'

def test_endpoint_obter_proprietario_retorna_404():
    service = SimpleNamespace(obter_por_numero_cadastro=AsyncMock(side_effect=ProprietarioNotFoundError('Proprietario nao encontrado')))
    app = FastAPI()
    app.include_router(proprietarios_router, prefix='/gestao-fundiaria')
    app.dependency_overrides[get_proprietario_service] = lambda: service
    client = TestClient(app)
    response = client.get('/gestao-fundiaria/proprietarios/PRP/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Proprietario nao encontrado'