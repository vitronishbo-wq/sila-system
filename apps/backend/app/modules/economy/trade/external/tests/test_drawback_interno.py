from __future__ import annotations
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.economy.trade.external.api.deps import get_drawback_interno_service
from app.modules.economy.trade.external.api.endpoints.drawback_interno import router as drawback_interno_router
from app.modules.economy.trade.external.application.services import DrawbackInternoService
from app.modules.economy.trade.external.domain.enums import StatusHabilitacao, TipoPessoa
from app.modules.economy.trade.external.exceptions import DrawbackInternoAlreadyExistsError, DrawbackInternoNotFoundError
from app.modules.economy.trade.external.infrastructure.repositories import InMemoryDrawbackInternoRepository

@pytest.mark.asyncio
async def test_service_fluxo_principal_drawback_interno():
    service = DrawbackInternoService(repository=InMemoryDrawbackInternoRepository())
    item = await service.solicitar(tipo_pessoa=TipoPessoa.JURIDICA, razao_social='Drawback Interno SA', cnpj_cpf='50020030000163', numero_processo='PROC-DRAW-INTN-2026-001', data_solicitacao=date(2026, 3, 15))
    assert item.status == StatusHabilitacao.PENDENTE
    item = await service.rejeitar(item.id, data_analise=date(2026, 3, 18), motivo='Pendencia documental')
    assert item.status == StatusHabilitacao.CANCELADO
    item = await service.reabrir(item.id)
    assert item.status == StatusHabilitacao.PENDENTE
    item = await service.aprovar(item.id, numero_radar='RADAR-DRAW-2026-5006', data_analise=date(2026, 3, 20), data_validade=date(2027, 3, 20))
    assert item.status == StatusHabilitacao.HABILITADO

@pytest.mark.asyncio
async def test_service_detecta_processo_duplicado_drawback_interno():
    service = DrawbackInternoService(repository=InMemoryDrawbackInternoRepository())
    payload = dict(tipo_pessoa=TipoPessoa.JURIDICA, razao_social='Duplicada Drawback Interno SA', cnpj_cpf='50020030000164', numero_processo='PROC-DRAW-INTN-2026-002', data_solicitacao=date(2026, 3, 15))
    await service.solicitar(**payload)
    with pytest.raises(DrawbackInternoAlreadyExistsError):
        await service.solicitar(**payload)

def test_endpoint_solicitar_drawback_interno_retorna_201():
    service = DrawbackInternoService(repository=InMemoryDrawbackInternoRepository())
    app = FastAPI()
    app.include_router(drawback_interno_router, prefix='/comercio_externo')
    app.dependency_overrides[get_drawback_interno_service] = lambda: service
    client = TestClient(app)
    response = client.post('/comercio_externo/drawback_interno/', json={'tipo_pessoa': 'juridica', 'razao_social': 'HTTP Drawback Interno SA', 'cnpj_cpf': '50020030000165', 'numero_processo': 'PROC-DRAW-INTN-2026-003', 'data_solicitacao': '2026-03-15'})
    assert response.status_code == 201
    assert response.json()['status'] == 'pendente'

def test_endpoint_obter_drawback_interno_retorna_404():
    service = SimpleNamespace(obter_por_id=AsyncMock(side_effect=DrawbackInternoNotFoundError('Drawback Interno nao encontrado')))
    app = FastAPI()
    app.include_router(drawback_interno_router, prefix='/comercio_externo')
    app.dependency_overrides[get_drawback_interno_service] = lambda: service
    client = TestClient(app)
    response = client.get(f'/comercio_externo/drawback_interno/{uuid4()}')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Drawback Interno nao encontrado'