from __future__ import annotations
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.resources.agricultura.api.deps import get_fitossanidade_service
from apps.backend.app.modules.resources.agricultura.api.endpoints.fitossanidade import router as fitossanidade_router
from apps.backend.app.modules.resources.agricultura.application.services.fitossanidade_service import FitossanidadeService
from apps.backend.app.modules.resources.agricultura.application.services.propriedade_service import PropriedadeService
from apps.backend.app.modules.resources.agricultura.domain.enums import SeveridadeOcorrencia, StatusOcorrencia, TipoPropriedade
from apps.backend.app.modules.resources.agricultura.exceptions import OcorrenciaNotFoundError

@pytest.mark.asyncio
async def test_fitossanidade_service_fluxo_ocorrencia():
    propriedade_service = PropriedadeService()
    prop = await propriedade_service.cadastrar(produtor_id=uuid4(), nome='Campo Verde', tipo=TipoPropriedade.PROPRIO, area_total_ha=30, area_cultivavel_ha=22)
    service = FitossanidadeService(propriedade_service=propriedade_service)
    oc = await service.registrar_ocorrencia(codigo_propriedade=prop.codigo_propriedade, praga_doenca='Lagarta', descricao='Ataque no talhao 2', severidade=SeveridadeOcorrencia.ALTA)
    assert oc.status == StatusOcorrencia.ABERTA
    oc = await service.iniciar_tratamento(oc.codigo_ocorrencia)
    assert oc.status == StatusOcorrencia.EM_TRATAMENTO
    oc = await service.resolver(oc.codigo_ocorrencia)
    assert oc.status == StatusOcorrencia.RESOLVIDA

def test_endpoint_registrar_ocorrencia_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), codigo_ocorrencia='FIT/2026/000001', codigo_propriedade='PROP/2026/000001', praga_doenca='Lagarta', descricao='Ataque no talhao 2', severidade='alta', status='aberta', data_registro='2026-02-28T00:00:00', cultura_afetada=None, acao_recomendada=None, data_resolucao=None)
    service = SimpleNamespace(registrar_ocorrencia=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(fitossanidade_router, prefix='/agricultura')
    app.dependency_overrides[get_fitossanidade_service] = lambda: service
    client = TestClient(app)
    response = client.post('/agricultura/fitossanidade/', json={'codigo_propriedade': 'PROP/2026/000001', 'praga_doenca': 'Lagarta', 'descricao': 'Ataque no talhao 2', 'severidade': 'alta'})
    assert response.status_code == 201
    assert response.json()['codigo_ocorrencia'] == 'FIT/2026/000001'

def test_endpoint_obter_ocorrencia_retorna_404():
    service = SimpleNamespace(obter=AsyncMock(side_effect=OcorrenciaNotFoundError('Ocorrencia fitossanitaria nao encontrada')))
    app = FastAPI()
    app.include_router(fitossanidade_router, prefix='/agricultura')
    app.dependency_overrides[get_fitossanidade_service] = lambda: service
    client = TestClient(app)
    response = client.get('/agricultura/fitossanidade/FIT/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Ocorrencia fitossanitaria nao encontrada'