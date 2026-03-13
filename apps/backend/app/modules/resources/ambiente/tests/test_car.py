from __future__ import annotations
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.resources.ambiente.api.deps import get_cadastro_service
from app.modules.resources.ambiente.api.endpoints.car import router as car_router
from app.modules.resources.ambiente.application.services.cadastro_service import CadastroService
from app.modules.resources.ambiente.domain.enums import Bioma, StatusCAR, TipoImovel
from app.modules.resources.ambiente.exceptions import CARNotFoundError
from app.modules.resources.ambiente.infrastructure.repositories import SQLAlchemyCARRepository, SQLAlchemyImovelRepository, SQLAlchemyProprietarioRepository

@pytest.mark.asyncio
async def test_cadastro_service_fluxo_car_sucesso():
    service = CadastroService(proprietario_repo=SQLAlchemyProprietarioRepository(), imovel_repo=SQLAlchemyImovelRepository(), car_repo=SQLAlchemyCARRepository())
    proprietario = await service.cadastrar_proprietario(nome='Maria Silva', documento='BI1234567', telefone='923000111')
    imovel = await service.cadastrar_imovel(proprietario_id=proprietario.id, nome='Fazenda Verde', provincia='Huambo', municipio='Caala', area_total=Decimal('150.0'), bioma=Bioma.SAVANA, tipo_imovel=TipoImovel.MEDIA_PROPRIEDADE)
    car = await service.criar_car(imovel_id=imovel.id, proprietario_id=proprietario.id, area_total=Decimal('150.0'), bioma=Bioma.SAVANA, tipo_imovel=TipoImovel.MEDIA_PROPRIEDADE)
    car = await service.atualizar_areas(numero_car=car.numero_car, area_preservacao_permanente=Decimal('20'), area_reserva_legal=Decimal('30'), area_uso_alternativo=Decimal('70'), area_consolidada=Decimal('20'))
    assert car.status == StatusCAR.PENDENTE
    car = await service.submeter_para_analise(car.numero_car)
    assert car.status == StatusCAR.EM_ANALISE
    car = await service.aprovar(car.numero_car, uuid4())
    assert car.status == StatusCAR.CADASTRADO

def test_endpoint_criar_car_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), numero_car='CAR/2026/000001', imovel_id=uuid4(), proprietario_id=uuid4(), area_total='150.00', area_preservacao_permanente='0', area_reserva_legal='0', area_uso_alternativo='0', area_consolidada='0', bioma='savana', tipo_imovel='media_propriedade', status='pendente', data_cadastro='2026-02-28', data_analise=None, data_aprovacao=None, analista_id=None, observacoes=None)
    service = SimpleNamespace(criar_car=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(car_router, prefix='/ambiente')
    app.dependency_overrides[get_cadastro_service] = lambda: service
    client = TestClient(app)
    response = client.post('/ambiente/car/', json={'imovel_id': str(uuid4()), 'proprietario_id': str(uuid4()), 'area_total': '150.00', 'bioma': 'savana', 'tipo_imovel': 'media_propriedade'})
    assert response.status_code == 201
    assert response.json()['numero_car'] == 'CAR/2026/000001'

def test_endpoint_obter_car_retorna_404():
    service = SimpleNamespace(obter_por_numero=AsyncMock(side_effect=CARNotFoundError('CAR nao encontrado')))
    app = FastAPI()
    app.include_router(car_router, prefix='/ambiente')
    app.dependency_overrides[get_cadastro_service] = lambda: service
    client = TestClient(app)
    response = client.get('/ambiente/car/CAR/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'CAR nao encontrado'