from __future__ import annotations
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.society.emprego.api.deps import get_candidato_service
from apps.backend.app.modules.society.emprego.api.endpoints.candidatos import router as candidatos_router
from apps.backend.app.modules.society.emprego.application.services.candidato_service import CandidatoService
from apps.backend.app.modules.society.emprego.domain.enums import Escolaridade, SituacaoProfissional, StatusCandidato
from apps.backend.app.modules.society.emprego.domain.models.candidato import Candidato
from apps.backend.app.modules.society.emprego.exceptions import CandidatoAlreadyExistsError, CitizenNotFoundError

def _build_service(candidato_repo, citizen_repo, request_service) -> CandidatoService:
    return CandidatoService(candidato_repo=candidato_repo, citizen_repo=citizen_repo, request_service=request_service)

@pytest.mark.asyncio
async def test_registrar_candidato_sucesso():
    citizen_id = uuid4()
    candidato_repo = SimpleNamespace(get_by_citizen=AsyncMock(return_value=None), next_numero_processo=AsyncMock(return_value='CAND/2026/0001'), save=AsyncMock(side_effect=lambda candidato: candidato))
    citizen_repo = SimpleNamespace(get_citizen=AsyncMock(return_value={'id': citizen_id}))
    request_service = SimpleNamespace(create_request=AsyncMock(return_value=uuid4()), complete_request=AsyncMock(return_value=True))
    service = _build_service(candidato_repo, citizen_repo, request_service)
    result = await service.registrar_candidato(citizen_id=citizen_id, escolaridade=Escolaridade.SECUNDARIA, situacao=SituacaoProfissional.DESEMPREGADO, areas_interesse=['administracao', 'vendas'])
    assert result.numero_processo == 'CAND/2026/0001'
    assert result.status == StatusCandidato.ATIVO
    candidato_repo.save.assert_awaited_once()
    request_service.create_request.assert_awaited_once()

@pytest.mark.asyncio
async def test_registrar_candidato_cidadao_inexistente():
    candidato_repo = SimpleNamespace(get_by_citizen=AsyncMock(return_value=None), next_numero_processo=AsyncMock(), save=AsyncMock())
    citizen_repo = SimpleNamespace(get_citizen=AsyncMock(return_value=None))
    request_service = SimpleNamespace(create_request=AsyncMock(), complete_request=AsyncMock())
    service = _build_service(candidato_repo, citizen_repo, request_service)
    with pytest.raises(CitizenNotFoundError):
        await service.registrar_candidato(citizen_id=uuid4(), escolaridade=Escolaridade.SECUNDARIA, situacao=SituacaoProfissional.DESEMPREGADO, areas_interesse=['administracao'])

@pytest.mark.asyncio
async def test_registrar_candidato_bloqueia_duplicado_ativo():
    citizen_id = uuid4()
    existente = Candidato.criar(citizen_id=citizen_id, escolaridade=Escolaridade.BASICA, situacao=SituacaoProfissional.EMPREGADO, areas_interesse=['logistica'], numero_processo='CAND/2026/0007')
    candidato_repo = SimpleNamespace(get_by_citizen=AsyncMock(return_value=existente), next_numero_processo=AsyncMock(), save=AsyncMock())
    citizen_repo = SimpleNamespace(get_citizen=AsyncMock(return_value={'id': citizen_id}))
    request_service = SimpleNamespace(create_request=AsyncMock(), complete_request=AsyncMock())
    service = _build_service(candidato_repo, citizen_repo, request_service)
    with pytest.raises(CandidatoAlreadyExistsError):
        await service.registrar_candidato(citizen_id=citizen_id, escolaridade=Escolaridade.SUPERIOR, situacao=SituacaoProfissional.DESEMPREGADO, areas_interesse=['tecnologia'])

@pytest.mark.asyncio
async def test_desativar_candidato_conclui_solicitacao():
    citizen_id = uuid4()
    actor_id = uuid4()
    candidato = Candidato.criar(citizen_id=citizen_id, escolaridade=Escolaridade.TECNICA, situacao=SituacaoProfissional.PRIMEIRO_EMPREGO, areas_interesse=['suporte'], numero_processo='CAND/2026/0011')
    candidato_repo = SimpleNamespace(get_by_id=AsyncMock(return_value=candidato), save=AsyncMock(side_effect=lambda item: item))
    citizen_repo = SimpleNamespace(get_citizen=AsyncMock())
    request_service = SimpleNamespace(create_request=AsyncMock(return_value=uuid4()), complete_request=AsyncMock(return_value=True))
    service = _build_service(candidato_repo, citizen_repo, request_service)
    updated = await service.desativar_candidato(candidato_id=candidato.id, motivo='Solicitado pelo candidato', actor_id=actor_id)
    assert updated.status == StatusCandidato.INATIVO
    assert updated.observacoes == 'Solicitado pelo candidato'
    request_service.complete_request.assert_awaited_once()

def _build_client(service) -> TestClient:
    app = FastAPI()
    app.include_router(candidatos_router, prefix='/emprego')
    app.dependency_overrides[get_candidato_service] = lambda: service
    return TestClient(app)

def test_endpoint_registrar_candidato_retorna_201():
    citizen_id = uuid4()
    candidato = Candidato.criar(citizen_id=citizen_id, escolaridade=Escolaridade.SECUNDARIA, situacao=SituacaoProfissional.DESEMPREGADO, areas_interesse=['administracao'], numero_processo='CAND/2026/0002')
    service = SimpleNamespace(registrar_candidato=AsyncMock(return_value=candidato))
    client = _build_client(service)
    response = client.post('/emprego/candidatos/', json={'citizen_id': str(citizen_id), 'escolaridade': 'secundaria', 'situacao': 'desempregado', 'areas_interesse': ['administracao']})
    assert response.status_code == 201
    payload = response.json()
    assert payload['numero_processo'] == 'CAND/2026/0002'
    assert payload['status'] == 'ativo'

def test_endpoint_registrar_candidato_retorna_404_para_cidadao_inexistente():
    service = SimpleNamespace(registrar_candidato=AsyncMock(side_effect=CitizenNotFoundError('Cidadao nao encontrado')))
    client = _build_client(service)
    response = client.post('/emprego/candidatos/', json={'citizen_id': str(uuid4()), 'escolaridade': 'secundaria', 'situacao': 'desempregado', 'areas_interesse': ['administracao']})
    assert response.status_code == 404
    assert 'nao encontrado' in response.json()['detail'].lower()