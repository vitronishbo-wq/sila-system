from __future__ import annotations
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.economy.trade.external.api.deps import get_habilitacao_exportador_service, get_habilitacao_importador_service, get_habilitacao_radar_service
from app.modules.economy.trade.external.api.endpoints.habilitacao_exportador import router as habilitacoes_exportador_router
from app.modules.economy.trade.external.api.endpoints.habilitacao_importador import router as habilitacoes_importador_router
from app.modules.economy.trade.external.api.endpoints.habilitacao_radar import router as habilitacao_radar_router
from app.modules.economy.trade.external.application.services import HabilitacaoExportadorService, HabilitacaoImportadorService, HabilitacaoRadarService
from app.modules.economy.trade.external.domain.enums import StatusHabilitacao, TipoPessoa
from app.modules.economy.trade.external.exceptions import HabilitacaoExportadorAlreadyExistsError, HabilitacaoExportadorNotFoundError, HabilitacaoImportadorAlreadyExistsError, HabilitacaoImportadorNotFoundError, HabilitacaoRadarAlreadyExistsError, HabilitacaoRadarNotFoundError
from app.modules.economy.trade.external.infrastructure.repositories import InMemoryHabilitacaoExportadorRepository, InMemoryHabilitacaoImportadorRepository, InMemoryHabilitacaoRadarRepository
CASES = ({'id': 'habilitacao_exportador', 'service_cls': HabilitacaoExportadorService, 'repository_cls': InMemoryHabilitacaoExportadorRepository, 'dependency': get_habilitacao_exportador_service, 'router': habilitacoes_exportador_router, 'already_exists_error_cls': HabilitacaoExportadorAlreadyExistsError, 'not_found_error_cls': HabilitacaoExportadorNotFoundError, 'base_url': '/comercio_externo/habilitacoes-exportador', 'processo': 'PROC-EXP-2026-001', 'cnpj': '50020030000140'}, {'id': 'habilitacao_importador', 'service_cls': HabilitacaoImportadorService, 'repository_cls': InMemoryHabilitacaoImportadorRepository, 'dependency': get_habilitacao_importador_service, 'router': habilitacoes_importador_router, 'already_exists_error_cls': HabilitacaoImportadorAlreadyExistsError, 'not_found_error_cls': HabilitacaoImportadorNotFoundError, 'base_url': '/comercio_externo/habilitacoes-importador', 'processo': 'PROC-IMP-2026-001', 'cnpj': '50020030000141'}, {'id': 'habilitacao_radar', 'service_cls': HabilitacaoRadarService, 'repository_cls': InMemoryHabilitacaoRadarRepository, 'dependency': get_habilitacao_radar_service, 'router': habilitacao_radar_router, 'already_exists_error_cls': HabilitacaoRadarAlreadyExistsError, 'not_found_error_cls': HabilitacaoRadarNotFoundError, 'base_url': '/comercio_externo/habilitacao_radar', 'processo': 'PROC-RADAR-2026-001', 'cnpj': '50020030000142'})

@pytest.mark.parametrize('case', CASES, ids=[case['id'] for case in CASES])
@pytest.mark.asyncio
async def test_service_fluxo_principal_habilitacao(case):
    service = case['service_cls'](repository=case['repository_cls']())
    item = await service.solicitar(tipo_pessoa=TipoPessoa.JURIDICA, razao_social=f'Empresa {case['id']}', cnpj_cpf=case['cnpj'], numero_processo=case['processo'], data_solicitacao=date(2026, 3, 10))
    assert item.status == StatusHabilitacao.PENDENTE
    item = await service.rejeitar(item.id, data_analise=date(2026, 3, 11), motivo='Pendencia documental')
    assert item.status == StatusHabilitacao.CANCELADO
    item = await service.reabrir(item.id)
    assert item.status == StatusHabilitacao.PENDENTE
    item = await service.aprovar(item.id, numero_radar='RADAR-2026-5000', data_analise=date(2026, 3, 12), data_validade=date(2027, 3, 12))
    assert item.status == StatusHabilitacao.HABILITADO

@pytest.mark.parametrize('case', CASES, ids=[case['id'] for case in CASES])
@pytest.mark.asyncio
async def test_service_detecta_processo_duplicado(case):
    service = case['service_cls'](repository=case['repository_cls']())
    payload = dict(tipo_pessoa=TipoPessoa.JURIDICA, razao_social=f'Duplicada {case['id']}', cnpj_cpf=case['cnpj'], numero_processo=case['processo'], data_solicitacao=date(2026, 3, 10))
    await service.solicitar(**payload)
    with pytest.raises(case['already_exists_error_cls']):
        await service.solicitar(**payload)

@pytest.mark.parametrize('case', CASES, ids=[case['id'] for case in CASES])
def test_endpoint_solicitar_retorna_201(case):
    service = case['service_cls'](repository=case['repository_cls']())
    app = FastAPI()
    app.include_router(case['router'], prefix='/comercio_externo')
    app.dependency_overrides[case['dependency']] = lambda: service
    client = TestClient(app)
    response = client.post(f'{case['base_url']}/', json={'tipo_pessoa': 'juridica', 'razao_social': f'HTTP {case['id']}', 'cnpj_cpf': case['cnpj'], 'numero_processo': case['processo'], 'data_solicitacao': '2026-03-10'})
    assert response.status_code == 201
    assert response.json()['status'] == 'pendente'

@pytest.mark.parametrize('case', CASES, ids=[case['id'] for case in CASES])
def test_endpoint_obter_retorna_404(case):
    service = SimpleNamespace(obter_por_id=AsyncMock(side_effect=case['not_found_error_cls']('Habilitacao nao encontrada')))
    app = FastAPI()
    app.include_router(case['router'], prefix='/comercio_externo')
    app.dependency_overrides[case['dependency']] = lambda: service
    client = TestClient(app)
    response = client.get(f'{case['base_url']}/{uuid4()}')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Habilitacao nao encontrada'