from __future__ import annotations
from datetime import date, timedelta
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.infrastructure.api.deps import get_projeto_service
from apps.backend.app.modules.infrastructure.api.endpoints.projetos import router as projetos_router
from apps.backend.app.modules.infrastructure.application.services.projeto_service import ProjetoService
from apps.backend.app.modules.infrastructure.domain.enums import StatusProjeto, TipoProjeto
from apps.backend.app.modules.infrastructure.core.exceptions import ProjetoNotFoundError
from apps.backend.app.modules.infrastructure.infrastructure.repositories import SQLAlchemyProjetoRepository

@pytest.mark.asyncio
async def test_projeto_service_fluxo_sucesso():
    service = ProjetoService(projeto_repo=SQLAlchemyProjetoRepository())
    item = await service.criar(nome='Projeto Executivo Escola Central', tipo=TipoProjeto.EXECUTIVO, orgao_responsavel_id=uuid4(), responsavel_tecnico_id=uuid4(), valor_estimado=Decimal('850000.00'), data_inicio_prevista=date.today(), data_fim_prevista=date.today() + timedelta(days=90))
    assert item.status == StatusProjeto.ELABORACAO
    assert item.codigo_projeto.startswith('PRJ/')
    item = await service.aprovar(item.codigo_projeto)
    assert item.status == StatusProjeto.APROVADO
    item = await service.iniciar_execucao(item.codigo_projeto, data_inicio=date.today())
    assert item.status == StatusProjeto.EM_EXECUCAO
    item = await service.revisar(item.codigo_projeto, motivo='Atualizacao tecnica')
    assert item.status == StatusProjeto.ELABORACAO
    assert item.versao == 2
    item = await service.aprovar(item.codigo_projeto)
    item = await service.iniciar_execucao(item.codigo_projeto, data_inicio=date.today())
    item = await service.concluir(item.codigo_projeto, data_fim=date.today() + timedelta(days=85))
    assert item.status == StatusProjeto.CONCLUIDO

def test_endpoint_criar_projeto_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), codigo_projeto='PRJ/2026/000001', nome='Projeto Executivo Escola Central', tipo=TipoProjeto.EXECUTIVO, status=StatusProjeto.ELABORACAO, orgao_responsavel_id=uuid4(), responsavel_tecnico_id=uuid4(), valor_estimado=Decimal('850000.00'), data_inicio_prevista=date(2026, 3, 1), data_fim_prevista=date(2026, 5, 30), data_cadastro=date(2026, 3, 1), obra_id=None, descricao=None, data_inicio_real=None, data_fim_real=None, versao=1, data_atualizacao=None, observacoes=None)
    service = SimpleNamespace(criar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(projetos_router, prefix='/obras-publicas')
    app.dependency_overrides[get_projeto_service] = lambda: service
    client = TestClient(app)
    response = client.post('/obras-publicas/projetos/', json={'nome': 'Projeto Executivo Escola Central', 'tipo': 'executivo', 'orgao_responsavel_id': str(uuid4()), 'responsavel_tecnico_id': str(uuid4()), 'valor_estimado': '850000.00', 'data_inicio_prevista': '2026-03-01', 'data_fim_prevista': '2026-05-30'})
    assert response.status_code == 201
    assert response.json()['codigo_projeto'] == 'PRJ/2026/000001'

def test_endpoint_obter_projeto_retorna_404():
    service = SimpleNamespace(obter_por_codigo=AsyncMock(side_effect=ProjetoNotFoundError('Projeto nao encontrado')))
    app = FastAPI()
    app.include_router(projetos_router, prefix='/obras-publicas')
    app.dependency_overrides[get_projeto_service] = lambda: service
    client = TestClient(app)
    response = client.get('/obras-publicas/projetos/PRJ/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Projeto nao encontrado'
