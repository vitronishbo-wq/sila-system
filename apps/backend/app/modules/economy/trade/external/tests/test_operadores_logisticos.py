from __future__ import annotations
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.economy.trade.external.api.deps import get_agente_carga_service, get_despachante_service, get_radar_service, get_transportador_internacional_service
from app.modules.economy.trade.external.api.endpoints.agente_carga import router as agentes_carga_router
from app.modules.economy.trade.external.api.endpoints.despachante import router as despachantes_router
from app.modules.economy.trade.external.api.endpoints.radar import router as radar_router
from app.modules.economy.trade.external.api.endpoints.transportador_internacional import router as transportadores_internacionais_router
from app.modules.economy.trade.external.application.services import AgenteCargaService, DespachanteService, RadarService, TransportadorInternacionalService
from app.modules.economy.trade.external.domain.enums import StatusHabilitacao, TipoPessoa
from app.modules.economy.trade.external.exceptions import AgenteCargaAlreadyExistsError, AgenteCargaNotFoundError, DespachanteAlreadyExistsError, DespachanteNotFoundError, RadarAlreadyExistsError, RadarNotFoundError, TransportadorInternacionalAlreadyExistsError, TransportadorInternacionalNotFoundError
from app.modules.economy.trade.external.infrastructure.repositories import InMemoryAgenteCargaRepository, InMemoryDespachanteRepository, InMemoryRadarRepository, InMemoryTransportadorInternacionalRepository
CASES = ({'id': 'despachante', 'service_cls': DespachanteService, 'repository_cls': InMemoryDespachanteRepository, 'dependency': get_despachante_service, 'router': despachantes_router, 'already_exists_error_cls': DespachanteAlreadyExistsError, 'not_found_error_cls': DespachanteNotFoundError, 'base_url': '/comercio_externo/despachantes', 'cnpj': '50020030000150'}, {'id': 'agente_carga', 'service_cls': AgenteCargaService, 'repository_cls': InMemoryAgenteCargaRepository, 'dependency': get_agente_carga_service, 'router': agentes_carga_router, 'already_exists_error_cls': AgenteCargaAlreadyExistsError, 'not_found_error_cls': AgenteCargaNotFoundError, 'base_url': '/comercio_externo/agentes-carga', 'cnpj': '50020030000149'}, {'id': 'transportador_internacional', 'service_cls': TransportadorInternacionalService, 'repository_cls': InMemoryTransportadorInternacionalRepository, 'dependency': get_transportador_internacional_service, 'router': transportadores_internacionais_router, 'already_exists_error_cls': TransportadorInternacionalAlreadyExistsError, 'not_found_error_cls': TransportadorInternacionalNotFoundError, 'base_url': '/comercio_externo/transportadores-internacionais', 'cnpj': '50020030000148'}, {'id': 'radar', 'service_cls': RadarService, 'repository_cls': InMemoryRadarRepository, 'dependency': get_radar_service, 'router': radar_router, 'already_exists_error_cls': RadarAlreadyExistsError, 'not_found_error_cls': RadarNotFoundError, 'base_url': '/comercio_externo/radar', 'cnpj': '50020030000147'})

@pytest.mark.parametrize('case', CASES, ids=[case['id'] for case in CASES])
@pytest.mark.asyncio
async def test_service_fluxo_principal(case):
    service = case['service_cls'](repository=case['repository_cls']())
    item = await service.cadastrar(razao_social=f'{case['id']} logistica', cnpj_cpf=case['cnpj'], tipo_pessoa=TipoPessoa.JURIDICA, endereco='Av. Porto', numero='100', bairro='Portuario', municipio='Lobito', provincia='Benguela', cep='2000-700')
    assert item.status == StatusHabilitacao.PENDENTE
    item = await service.habilitar(item.id, numero_radar='RADAR-2026-3000', data_habilitacao=date(2026, 3, 4), data_validade=date(2027, 3, 4))
    assert item.status == StatusHabilitacao.HABILITADO
    item = await service.suspender(item.id, data_suspensao=date(2026, 8, 10), motivo='Auditoria interna')
    assert item.status == StatusHabilitacao.SUSPENSO
    item = await service.reabilitar(item.id)
    assert item.status == StatusHabilitacao.HABILITADO
    item = await service.cancelar(item.id, data_cancelamento=date(2026, 12, 15), motivo='Encerramento das operacoes')
    assert item.status == StatusHabilitacao.CANCELADO

@pytest.mark.parametrize('case', CASES, ids=[case['id'] for case in CASES])
@pytest.mark.asyncio
async def test_service_detecta_cnpj_cpf_duplicado(case):
    service = case['service_cls'](repository=case['repository_cls']())
    payload = dict(razao_social=f'Duplicado {case['id']}', cnpj_cpf=case['cnpj'], tipo_pessoa=TipoPessoa.JURIDICA, endereco='Rua A', numero='10', bairro='Centro', municipio='Luanda', provincia='Luanda', cep='1000-900')
    await service.cadastrar(**payload)
    with pytest.raises(case['already_exists_error_cls']):
        await service.cadastrar(**payload)

@pytest.mark.parametrize('case', CASES, ids=[case['id'] for case in CASES])
def test_endpoint_cadastrar_retorna_201(case):
    service = case['service_cls'](repository=case['repository_cls']())
    app = FastAPI()
    app.include_router(case['router'], prefix='/comercio_externo')
    app.dependency_overrides[case['dependency']] = lambda: service
    client = TestClient(app)
    response = client.post(f'{case['base_url']}/', json={'razao_social': f'HTTP {case['id']}', 'cnpj_cpf': case['cnpj'], 'tipo_pessoa': 'juridica', 'endereco': 'Av. Marginal', 'numero': '1', 'bairro': 'Ingombota', 'municipio': 'Luanda', 'provincia': 'Luanda', 'cep': '1000-200'})
    assert response.status_code == 201
    assert response.json()['status'] == 'pendente'

@pytest.mark.parametrize('case', CASES, ids=[case['id'] for case in CASES])
def test_endpoint_obter_por_id_retorna_404(case):
    service = SimpleNamespace(obter_por_id=AsyncMock(side_effect=case['not_found_error_cls']('Registro nao encontrado')))
    app = FastAPI()
    app.include_router(case['router'], prefix='/comercio_externo')
    app.dependency_overrides[case['dependency']] = lambda: service
    client = TestClient(app)
    response = client.get(f'{case['base_url']}/{uuid4()}')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Registro nao encontrado'