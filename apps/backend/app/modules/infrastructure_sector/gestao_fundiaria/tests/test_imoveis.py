from __future__ import annotations
from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.api.deps import get_imovel_service
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.api.endpoints.imoveis import router as imoveis_router
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.services.imovel_service import ImovelService
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import NaturezaImovel, RegimePropriedade, SituacaoDominial, TipoImovel
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.exceptions import ImovelNotFoundError
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.repositories import SQLAlchemyImovelRepository

@pytest.mark.asyncio
async def test_imovel_service_fluxo_sucesso():
    service = ImovelService(imovel_repo=SQLAlchemyImovelRepository())
    item = await service.cadastrar(tipo=TipoImovel.URBANO, natureza=NaturezaImovel.PRIVADO, area_total=Decimal('500.00'), endereco='Rua A, 10', bairro='Maianga', municipio='Luanda', provincia='Luanda')
    assert item.situacao == SituacaoDominial.REGULAR
    assert item.inscricao_imobiliaria.startswith('IMV/')
    item = await service.atualizar_area(item.inscricao_imobiliaria, area_total=Decimal('525.00'))
    assert item.area_total == Decimal('525.00')
    proprietario_id = uuid4()
    item = await service.atualizar_proprietario(item.inscricao_imobiliaria, proprietario_id=proprietario_id)
    assert item.proprietario_atual_id == proprietario_id

def test_endpoint_cadastrar_imovel_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), inscricao_imobiliaria='IMV/2026/000001', tipo=TipoImovel.URBANO, natureza=NaturezaImovel.PRIVADO, regime=RegimePropriedade.PLENA, situacao=SituacaoDominial.REGULAR, area_total=Decimal('500.00'), endereco='Rua A, 10', bairro='Maianga', municipio='Luanda', provincia='Luanda', data_cadastro=date(2026, 3, 1), area_privativa=None, area_construida=None, area_terreno=None, cep=None, coordenadas_lat=None, coordenadas_long=None, matricula_id=None, proprietario_atual_id=None, data_atualizacao=None, ativo=True, observacoes=None)
    service = SimpleNamespace(cadastrar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(imoveis_router, prefix='/gestao-fundiaria')
    app.dependency_overrides[get_imovel_service] = lambda: service
    client = TestClient(app)
    response = client.post('/gestao-fundiaria/imoveis/', json={'tipo': 'urbano', 'natureza': 'privado', 'area_total': '500.00', 'endereco': 'Rua A, 10', 'bairro': 'Maianga', 'municipio': 'Luanda', 'provincia': 'Luanda'})
    assert response.status_code == 201
    assert response.json()['inscricao_imobiliaria'] == 'IMV/2026/000001'

def test_endpoint_obter_imovel_retorna_404():
    service = SimpleNamespace(obter_por_inscricao=AsyncMock(side_effect=ImovelNotFoundError('Imovel nao encontrado')))
    app = FastAPI()
    app.include_router(imoveis_router, prefix='/gestao-fundiaria')
    app.dependency_overrides[get_imovel_service] = lambda: service
    client = TestClient(app)
    response = client.get('/gestao-fundiaria/imoveis/IMV/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Imovel nao encontrado'