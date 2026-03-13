from __future__ import annotations
from datetime import date, timedelta
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.resources.ambiente.api.deps import get_condicionante_service, get_estudo_service
from apps.backend.app.modules.resources.ambiente.api.endpoints.condicionantes import router as condicionantes_router
from apps.backend.app.modules.resources.ambiente.api.endpoints.estudos import router as estudos_router
from apps.backend.app.modules.resources.ambiente.application.services.cadastro_service import CadastroService
from apps.backend.app.modules.resources.ambiente.application.services.condicionante_service import CondicionanteService
from apps.backend.app.modules.resources.ambiente.application.services.estudo_service import EstudoService
from apps.backend.app.modules.resources.ambiente.application.services.licenciamento_service import LicenciamentoService
from apps.backend.app.modules.resources.ambiente.domain.enums import Bioma, StatusCondicionante, StatusEstudoAmbiental, StatusLicenca, TipoEstudoAmbiental, TipoImovel, TipoLicenca
from apps.backend.app.modules.resources.ambiente.exceptions import CondicionanteNotFoundError, EstudoNotFoundError
from apps.backend.app.modules.resources.ambiente.infrastructure.repositories import SQLAlchemyCARRepository, SQLAlchemyCondicionanteRepository, SQLAlchemyEstudoRepository, SQLAlchemyImovelRepository, SQLAlchemyLicencaRepository, SQLAlchemyProprietarioRepository

@pytest.mark.asyncio
async def test_fluxo_estudo_e_condicionante_sucesso():
    proprietario_repo = SQLAlchemyProprietarioRepository()
    imovel_repo = SQLAlchemyImovelRepository()
    car_repo = SQLAlchemyCARRepository()
    licenca_repo = SQLAlchemyLicencaRepository()
    estudo_repo = SQLAlchemyEstudoRepository()
    condicionante_repo = SQLAlchemyCondicionanteRepository()
    cadastro_service = CadastroService(proprietario_repo=proprietario_repo, imovel_repo=imovel_repo, car_repo=car_repo)
    licenciamento_service = LicenciamentoService(car_repo=car_repo, licenca_repo=licenca_repo)
    estudo_service = EstudoService(licenca_repo=licenca_repo, estudo_repo=estudo_repo)
    condicionante_service = CondicionanteService(licenca_repo=licenca_repo, condicionante_repo=condicionante_repo)
    proprietario = await cadastro_service.cadastrar_proprietario(nome='Domingos Miala', documento='BI1234500')
    imovel = await cadastro_service.cadastrar_imovel(proprietario_id=proprietario.id, nome='Fazenda Rio Azul', provincia='Benguela', municipio='Lobito', area_total=Decimal('120'), bioma=Bioma.SAVANA, tipo_imovel=TipoImovel.MEDIA_PROPRIEDADE)
    car = await cadastro_service.criar_car(imovel_id=imovel.id, proprietario_id=proprietario.id, area_total=Decimal('120'), bioma=Bioma.SAVANA, tipo_imovel=TipoImovel.MEDIA_PROPRIEDADE)
    car = await cadastro_service.submeter_para_analise(car.numero_car)
    car = await cadastro_service.aprovar(car.numero_car, uuid4())
    licenca = await licenciamento_service.requerer_licenca(numero_car=car.numero_car, tipo=TipoLicenca.PREVIA, atividade='Projeto de agroindustria')
    licenca = await licenciamento_service.iniciar_analise(licenca.numero_licenca)
    licenca = await licenciamento_service.deferir(licenca.numero_licenca, analista_id=uuid4(), data_validade=date.today() + timedelta(days=365))
    estudo = await estudo_service.submeter(numero_licenca=licenca.numero_licenca, tipo=TipoEstudoAmbiental.EIA, descricao='EIA da planta de processamento', responsavel_tecnico='Eng. Ambiental Kunda')
    assert estudo.status == StatusEstudoAmbiental.SUBMETIDO
    estudo = await estudo_service.iniciar_analise(estudo.numero_estudo)
    assert estudo.status == StatusEstudoAmbiental.EM_ANALISE
    estudo = await estudo_service.aprovar(estudo.numero_estudo, uuid4())
    assert estudo.status == StatusEstudoAmbiental.APROVADO
    condicionante = await condicionante_service.criar(numero_licenca=licenca.numero_licenca, descricao='Implantar faixa de protecao ciliar', prazo_dias=180)
    assert condicionante.status == StatusCondicionante.PENDENTE
    condicionante = await condicionante_service.iniciar_cumprimento(condicionante.codigo_condicionante)
    assert condicionante.status == StatusCondicionante.EM_CUMPRIMENTO
    condicionante = await condicionante_service.registrar_cumprimento(condicionante.codigo_condicionante, evidencia='Relatorio fotografico')
    assert condicionante.status == StatusCondicionante.CUMPRIDA

def test_endpoint_submeter_estudo_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), numero_estudo='EST/2026/000001', numero_licenca='LIC/2026/000001', tipo=TipoEstudoAmbiental.EIA, descricao='Estudo de impacto da captação', responsavel_tecnico='Tecnico A', status=StatusEstudoAmbiental.SUBMETIDO, data_submissao=date(2026, 2, 28), data_analise=None, data_aprovacao=None, analista_id=None, observacoes=None)
    service = SimpleNamespace(submeter=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(estudos_router, prefix='/ambiente')
    app.dependency_overrides[get_estudo_service] = lambda: service
    client = TestClient(app)
    response = client.post('/ambiente/estudos/', json={'numero_licenca': 'LIC/2026/000001', 'tipo': 'eia', 'descricao': 'Estudo de impacto da captação', 'responsavel_tecnico': 'Tecnico A'})
    assert response.status_code == 201
    assert response.json()['numero_estudo'] == 'EST/2026/000001'

def test_endpoint_obter_estudo_retorna_404():
    service = SimpleNamespace(obter_por_numero=AsyncMock(side_effect=EstudoNotFoundError('Estudo ambiental nao encontrado')))
    app = FastAPI()
    app.include_router(estudos_router, prefix='/ambiente')
    app.dependency_overrides[get_estudo_service] = lambda: service
    client = TestClient(app)
    response = client.get('/ambiente/estudos/EST/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Estudo ambiental nao encontrado'

def test_endpoint_criar_condicionante_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), codigo_condicionante='COND/2026/000001', numero_licenca='LIC/2026/000001', descricao='Implementar monitoramento trimestral', prazo_dias=90, status=StatusCondicionante.PENDENTE, data_criacao=date(2026, 2, 28), data_limite=date(2026, 5, 29), data_cumprimento=None, evidencia=None, observacoes=None)
    service = SimpleNamespace(criar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(condicionantes_router, prefix='/ambiente')
    app.dependency_overrides[get_condicionante_service] = lambda: service
    client = TestClient(app)
    response = client.post('/ambiente/condicionantes/', json={'numero_licenca': 'LIC/2026/000001', 'descricao': 'Implementar monitoramento trimestral', 'prazo_dias': 90})
    assert response.status_code == 201
    assert response.json()['codigo_condicionante'] == 'COND/2026/000001'

def test_endpoint_obter_condicionante_retorna_404():
    service = SimpleNamespace(obter_por_codigo=AsyncMock(side_effect=CondicionanteNotFoundError('Condicionante nao encontrada')))
    app = FastAPI()
    app.include_router(condicionantes_router, prefix='/ambiente')
    app.dependency_overrides[get_condicionante_service] = lambda: service
    client = TestClient(app)
    response = client.get('/ambiente/condicionantes/COND/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Condicionante nao encontrada'