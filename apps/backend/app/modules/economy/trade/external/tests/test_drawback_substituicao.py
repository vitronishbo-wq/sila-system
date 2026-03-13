from __future__ import annotations
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.economy.trade.external.api.deps import get_drawback_substituicao_service
from app.modules.economy.trade.external.api.endpoints.drawback_substituicao import router as drawback_substituicao_router
from app.modules.economy.trade.external.application.services import DrawbackSubstituicaoService
from app.modules.economy.trade.external.domain.enums import StatusHabilitacao, TipoPessoa
from app.modules.economy.trade.external.exceptions import DrawbackSubstituicaoAlreadyExistsError, DrawbackSubstituicaoNotFoundError
from app.modules.economy.trade.external.infrastructure.repositories import InMemoryDrawbackSubstituicaoRepository

@pytest.mark.asyncio
async def test_service_fluxo_principal_drawback_substituicao():
    service = DrawbackSubstituicaoService(repository=InMemoryDrawbackSubstituicaoRepository())
    item = await service.solicitar(tipo_pessoa=TipoPessoa.JURIDICA, razao_social='Drawback Substituicao SA', cnpj_cpf='50020030000154', numero_processo='PROC-DRAW-SUB-2026-001', data_solicitacao=date(2026, 3, 15))
    assert item.status == StatusHabilitacao.PENDENTE
    item = await service.rejeitar(item.id, data_analise=date(2026, 3, 18), motivo='Pendencia documental')
    assert item.status == StatusHabilitacao.CANCELADO
    item = await service.reabrir(item.id)
    assert item.status == StatusHabilitacao.PENDENTE
    item = await service.aprovar(item.id, numero_radar='RADAR-DRAW-2026-5003', data_analise=date(2026, 3, 20), data_validade=date(2027, 3, 20))
    assert item.status == StatusHabilitacao.HABILITADO

@pytest.mark.asyncio
async def test_service_detecta_processo_duplicado_drawback_substituicao():
    service = DrawbackSubstituicaoService(repository=InMemoryDrawbackSubstituicaoRepository())
    payload = dict(tipo_pessoa=TipoPessoa.JURIDICA, razao_social='Duplicada Drawback Substituicao SA', cnpj_cpf='50020030000155', numero_processo='PROC-DRAW-SUB-2026-002', data_solicitacao=date(2026, 3, 15))
    await service.solicitar(**payload)
    with pytest.raises(DrawbackSubstituicaoAlreadyExistsError):
        await service.solicitar(**payload)

def test_endpoint_solicitar_drawback_substituicao_retorna_201():
    service = DrawbackSubstituicaoService(repository=InMemoryDrawbackSubstituicaoRepository())
    app = FastAPI()
    app.include_router(drawback_substituicao_router, prefix='/comercio_externo')
    app.dependency_overrides[get_drawback_substituicao_service] = lambda: service
    client = TestClient(app)
    response = client.post('/comercio_externo/drawback_substituicao/', json={'tipo_pessoa': 'juridica', 'razao_social': 'HTTP Drawback Substituicao SA', 'cnpj_cpf': '50020030000156', 'numero_processo': 'PROC-DRAW-SUB-2026-003', 'data_solicitacao': '2026-03-15'})
    assert response.status_code == 201
    assert response.json()['status'] == 'pendente'

def test_endpoint_obter_drawback_substituicao_retorna_404():
    service = SimpleNamespace(obter_por_id=AsyncMock(side_effect=DrawbackSubstituicaoNotFoundError('Drawback Substituicao nao encontrada')))
    app = FastAPI()
    app.include_router(drawback_substituicao_router, prefix='/comercio_externo')
    app.dependency_overrides[get_drawback_substituicao_service] = lambda: service
    client = TestClient(app)
    response = client.get(f'/comercio_externo/drawback_substituicao/{uuid4()}')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Drawback Substituicao nao encontrada'