from __future__ import annotations
from datetime import date, timedelta
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.resources.ambiente.api.deps import get_fiscalizacao_service
from app.modules.resources.ambiente.api.endpoints.fiscalizacoes import router as fiscalizacoes_router
from app.modules.resources.ambiente.application.services.cadastro_service import CadastroService
from app.modules.resources.ambiente.application.services.fiscalizacao_service import FiscalizacaoService
from app.modules.resources.ambiente.application.services.licenciamento_service import LicenciamentoService
from app.modules.resources.ambiente.domain.enums import Bioma, StatusFiscalizacao, StatusLicenca, TipoImovel, TipoLicenca
from app.modules.resources.ambiente.exceptions import FiscalizacaoNotFoundError
from app.modules.resources.ambiente.infrastructure.repositories import SQLAlchemyCARRepository, SQLAlchemyFiscalizacaoRepository, SQLAlchemyImovelRepository, SQLAlchemyLicencaRepository, SQLAlchemyProprietarioRepository

@pytest.mark.asyncio
async def test_fiscalizacao_service_fluxo_sucesso():
    proprietario_repo = SQLAlchemyProprietarioRepository()
    imovel_repo = SQLAlchemyImovelRepository()
    car_repo = SQLAlchemyCARRepository()
    licenca_repo = SQLAlchemyLicencaRepository()
    fiscalizacao_repo = SQLAlchemyFiscalizacaoRepository()
    cadastro_service = CadastroService(proprietario_repo=proprietario_repo, imovel_repo=imovel_repo, car_repo=car_repo)
    licenciamento_service = LicenciamentoService(car_repo=car_repo, licenca_repo=licenca_repo)
    fiscalizacao_service = FiscalizacaoService(licenca_repo=licenca_repo, fiscalizacao_repo=fiscalizacao_repo)
    proprietario = await cadastro_service.cadastrar_proprietario(nome='Fatima Cangola', documento='BI11223344')
    imovel = await cadastro_service.cadastrar_imovel(proprietario_id=proprietario.id, nome='Fazenda Nova Vida', provincia='Huila', municipio='Lubango', area_total=Decimal('80'), bioma=Bioma.SAVANA, tipo_imovel=TipoImovel.PEQUENA_PROPRIEDADE)
    car = await cadastro_service.criar_car(imovel_id=imovel.id, proprietario_id=proprietario.id, area_total=Decimal('80'), bioma=Bioma.SAVANA, tipo_imovel=TipoImovel.PEQUENA_PROPRIEDADE)
    car = await cadastro_service.submeter_para_analise(car.numero_car)
    car = await cadastro_service.aprovar(car.numero_car, uuid4())
    licenca = await licenciamento_service.requerer_licenca(numero_car=car.numero_car, tipo=TipoLicenca.PREVIA, atividade='Ampliação de área produtiva')
    licenca = await licenciamento_service.iniciar_analise(licenca.numero_licenca)
    licenca = await licenciamento_service.deferir(licenca.numero_licenca, analista_id=uuid4(), data_validade=date.today() + timedelta(days=365))
    assert licenca.status == StatusLicenca.DEFERIDA
    fiscalizacao = await fiscalizacao_service.agendar(numero_licenca=licenca.numero_licenca, localidade='Perimetro Sul', objetivo='Verificar cumprimento de condicionantes', fiscal_responsavel='Fiscal A', data_agendada=date.today())
    assert fiscalizacao.status == StatusFiscalizacao.AGENDADA
    fiscalizacao = await fiscalizacao_service.iniciar(fiscalizacao.numero_fiscalizacao)
    assert fiscalizacao.status == StatusFiscalizacao.EM_ANDAMENTO
    fiscalizacao = await fiscalizacao_service.concluir(fiscalizacao.numero_fiscalizacao, 'Nao foram identificadas irregularidades graves')
    assert fiscalizacao.status == StatusFiscalizacao.CONCLUIDA

def test_endpoint_agendar_fiscalizacao_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), numero_fiscalizacao='FIS/2026/000001', numero_licenca='LIC/2026/000001', localidade='Perimetro Sul', objetivo='Fiscalizacao ordinaria', fiscal_responsavel='Fiscal A', status=StatusFiscalizacao.AGENDADA, data_agendada=date(2026, 2, 28), data_realizacao=None, relatorio=None, observacoes=None)
    service = SimpleNamespace(agendar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(fiscalizacoes_router, prefix='/ambiente')
    app.dependency_overrides[get_fiscalizacao_service] = lambda: service
    client = TestClient(app)
    response = client.post('/ambiente/fiscalizacoes/', json={'numero_licenca': 'LIC/2026/000001', 'localidade': 'Perimetro Sul', 'objetivo': 'Fiscalizacao ordinaria', 'fiscal_responsavel': 'Fiscal A', 'data_agendada': '2026-02-28'})
    assert response.status_code == 201
    assert response.json()['numero_fiscalizacao'] == 'FIS/2026/000001'

def test_endpoint_obter_fiscalizacao_retorna_404():
    service = SimpleNamespace(obter_por_numero=AsyncMock(side_effect=FiscalizacaoNotFoundError('Fiscalizacao nao encontrada')))
    app = FastAPI()
    app.include_router(fiscalizacoes_router, prefix='/ambiente')
    app.dependency_overrides[get_fiscalizacao_service] = lambda: service
    client = TestClient(app)
    response = client.get('/ambiente/fiscalizacoes/FIS/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Fiscalizacao nao encontrada'