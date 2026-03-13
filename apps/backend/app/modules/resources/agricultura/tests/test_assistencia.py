from __future__ import annotations
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.resources.agricultura.api.deps import get_assistencia_service
from app.modules.resources.agricultura.api.endpoints.assistencia import router as assistencia_router
from app.modules.resources.agricultura.application.services.assistencia_service import AssistenciaService
from app.modules.resources.agricultura.application.services.propriedade_service import PropriedadeService
from app.modules.resources.agricultura.domain.enums import StatusAssistencia, TipoPropriedade
from app.modules.resources.agricultura.exceptions import AssistenciaNotFoundError

@pytest.mark.asyncio
async def test_assistencia_service_fluxo_agendar_concluir():
    propriedade_service = PropriedadeService()
    prop = await propriedade_service.cadastrar(produtor_id=uuid4(), nome='Fazenda Oeste', tipo=TipoPropriedade.PROPRIO, area_total_ha=55, area_cultivavel_ha=40)
    service = AssistenciaService(propriedade_service=propriedade_service)
    item = await service.agendar(codigo_propriedade=prop.codigo_propriedade, tecnico_nome='Eng. Antonio', objetivo='Avaliacao de solo')
    assert item.status == StatusAssistencia.AGENDADA
    item = await service.concluir(item.codigo_assistencia, recomendacoes='Aplicar corretivo em 30 dias')
    assert item.status == StatusAssistencia.REALIZADA
    assert item.recomendacoes == 'Aplicar corretivo em 30 dias'

def test_endpoint_agendar_assistencia_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), codigo_assistencia='AST/2026/000001', codigo_propriedade='PROP/2026/000001', tecnico_nome='Eng. Antonio', objetivo='Avaliacao de solo', status='agendada', data_agendamento='2026-02-28', data_realizacao=None, recomendacoes=None, motivo_cancelamento=None)
    service = SimpleNamespace(agendar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(assistencia_router, prefix='/agricultura')
    app.dependency_overrides[get_assistencia_service] = lambda: service
    client = TestClient(app)
    response = client.post('/agricultura/assistencia/', json={'codigo_propriedade': 'PROP/2026/000001', 'tecnico_nome': 'Eng. Antonio', 'objetivo': 'Avaliacao de solo'})
    assert response.status_code == 201
    assert response.json()['codigo_assistencia'] == 'AST/2026/000001'

def test_endpoint_obter_assistencia_retorna_404():
    service = SimpleNamespace(obter=AsyncMock(side_effect=AssistenciaNotFoundError('Assistencia tecnica nao encontrada')))
    app = FastAPI()
    app.include_router(assistencia_router, prefix='/agricultura')
    app.dependency_overrides[get_assistencia_service] = lambda: service
    client = TestClient(app)
    response = client.get('/agricultura/assistencia/AST/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Assistencia tecnica nao encontrada'