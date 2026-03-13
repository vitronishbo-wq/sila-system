from __future__ import annotations
from datetime import date, timedelta
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.deps import get_operacao_urbana_service
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.api.endpoints.operacoes_urbanas import router as operacoes_urbanas_router
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.services.operacao_urbana_service import OperacaoUrbanaService
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusOperacaoUrbana, TipoOperacaoUrbana
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.exceptions import OperacaoUrbanaNotFoundError
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.repositories import SQLAlchemyOperacaoUrbanaRepository

@pytest.mark.asyncio
async def test_operacao_urbana_service_fluxo_sucesso():
    service = OperacaoUrbanaService(operacao_urbana_repo=SQLAlchemyOperacaoUrbanaRepository())
    item = await service.criar(nome='Operacao Integrada Marginal Sul', tipo=TipoOperacaoUrbana.OPERACAO_URBANA_CONSORCIADA, plano_diretor_id=uuid4(), orgao_responsavel_id=uuid4(), provincia='Luanda', municipio='Luanda', investimento_previsto=Decimal('150000000.00'))
    assert item.status == StatusOperacaoUrbana.ELABORACAO
    assert item.codigo_operacao.startswith('OPU/')
    item = await service.aprovar(item.codigo_operacao)
    assert item.status == StatusOperacaoUrbana.APROVADA
    item = await service.iniciar_execucao(item.codigo_operacao, data_inicio_real=date.today())
    assert item.status == StatusOperacaoUrbana.EM_EXECUCAO
    item = await service.atualizar_execucao(item.codigo_operacao, percentual_execucao=Decimal('42.50'), investimento_executado=Decimal('45000000.00'))
    assert item.percentual_execucao == Decimal('42.50')
    item = await service.suspender(item.codigo_operacao, motivo='Ajuste contratual')
    assert item.status == StatusOperacaoUrbana.SUSPENSA
    item = await service.retomar(item.codigo_operacao)
    assert item.status == StatusOperacaoUrbana.EM_EXECUCAO
    item = await service.concluir(item.codigo_operacao, data_fim_real=date.today() + timedelta(days=1))
    assert item.status == StatusOperacaoUrbana.CONCLUIDA

def test_endpoint_criar_operacao_urbana_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), codigo_operacao='OPU/2026/000001', nome='Operacao Integrada Marginal Sul', tipo=TipoOperacaoUrbana.OPERACAO_URBANA_CONSORCIADA, status=StatusOperacaoUrbana.ELABORACAO, plano_diretor_id=uuid4(), orgao_responsavel_id=uuid4(), provincia='Luanda', municipio='Luanda', area_intervencao=None, investimento_previsto=Decimal('150000000.00'), investimento_executado=None, data_inicio_prevista=None, data_fim_prevista=None, data_inicio_real=None, data_fim_real=None, percentual_execucao=Decimal('0'), data_cadastro=date(2026, 3, 1), data_atualizacao=None, observacoes=None)
    service = SimpleNamespace(criar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(operacoes_urbanas_router, prefix='/urbanismo-habitacao')
    app.dependency_overrides[get_operacao_urbana_service] = lambda: service
    client = TestClient(app)
    response = client.post('/urbanismo-habitacao/operacoes-urbanas/', json={'nome': 'Operacao Integrada Marginal Sul', 'tipo': 'operacao_urbana_consorciada', 'plano_diretor_id': str(uuid4()), 'orgao_responsavel_id': str(uuid4()), 'provincia': 'Luanda', 'municipio': 'Luanda', 'investimento_previsto': '150000000.00'})
    assert response.status_code == 201
    assert response.json()['codigo_operacao'] == 'OPU/2026/000001'

def test_endpoint_obter_operacao_urbana_retorna_404():
    service = SimpleNamespace(obter_por_codigo=AsyncMock(side_effect=OperacaoUrbanaNotFoundError('Operacao urbana nao encontrada')))
    app = FastAPI()
    app.include_router(operacoes_urbanas_router, prefix='/urbanismo-habitacao')
    app.dependency_overrides[get_operacao_urbana_service] = lambda: service
    client = TestClient(app)
    response = client.get('/urbanismo-habitacao/operacoes-urbanas/OPU/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Operacao urbana nao encontrada'