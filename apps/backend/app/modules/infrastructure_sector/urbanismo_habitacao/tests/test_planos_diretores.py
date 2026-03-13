from __future__ import annotations
from datetime import date, timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.infrastructure_sector.urbanismo_habitacao.api.deps import get_plano_diretor_service
from app.modules.infrastructure_sector.urbanismo_habitacao.api.endpoints.planos_diretores import router as planos_diretores_router
from app.modules.infrastructure_sector.urbanismo_habitacao.application.services.plano_diretor_service import PlanoDiretorService
from app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusPlanoDiretor, TipoPlanoDiretor
from app.modules.infrastructure_sector.urbanismo_habitacao.exceptions import PlanoDiretorNotFoundError
from app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.repositories import SQLAlchemyPlanoDiretorRepository

@pytest.mark.asyncio
async def test_plano_diretor_service_fluxo_sucesso():
    service = PlanoDiretorService(plano_diretor_repo=SQLAlchemyPlanoDiretorRepository())
    item = await service.criar(nome='Plano Diretor de Luanda 2035', tipo=TipoPlanoDiretor.MUNICIPAL, provincia='Luanda', ano_elaboracao=2026, orgao_responsavel_id=uuid4(), municipio='Luanda')
    assert item.status == StatusPlanoDiretor.ELABORACAO
    assert item.codigo_plano.startswith('PD/')
    item = await service.iniciar_consulta_publica(item.codigo_plano)
    assert item.status == StatusPlanoDiretor.CONSULTA_PUBLICA
    item = await service.realizar_audiencia_publica(item.codigo_plano, participantes=120)
    assert item.status == StatusPlanoDiretor.AUDIENCIA_PUBLICA
    assert item.audiencias_publicas == 1
    assert item.participantes_consulta == 120
    item = await service.aprovar_camara(item.codigo_plano, lei_aprovacao='Lei Municipal 12/2026', ano_aprovacao=2026)
    assert item.status == StatusPlanoDiretor.APROVADO_CAMARA
    item = await service.aprovar_prefeitura(item.codigo_plano)
    assert item.status == StatusPlanoDiretor.APROVADO_PREFEITURA
    item = await service.sancionar(item.codigo_plano, data_publicacao=date.today())
    assert item.status == StatusPlanoDiretor.SANCIONADO
    item = await service.publicar(item.codigo_plano)
    assert item.status == StatusPlanoDiretor.PUBLICADO
    item = await service.definir_validade(item.codigo_plano, data_inicio=date.today(), data_fim=date.today() + timedelta(days=3650))
    assert item.periodo_validade_fim == date.today() + timedelta(days=3650)

def test_endpoint_criar_plano_diretor_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), codigo_plano='PD/2026/000001', nome='Plano Diretor de Luanda 2035', tipo=TipoPlanoDiretor.MUNICIPAL, status=StatusPlanoDiretor.ELABORACAO, provincia='Luanda', ano_elaboracao=2026, orgao_responsavel_id=uuid4(), municipio='Luanda', ano_aprovacao=None, ano_publicacao=None, periodo_validade_inicio=None, periodo_validade_fim=None, lei_aprovacao=None, participantes_consulta=None, audiencias_publicas=None, documento_url=None, mapa_url=None, area_total_urbana=None, area_total_rural=None, populacao_estimada=None, densidade_media=None, macrozoneamento=None, diretrizes_gerais=None, objetivos_estrategicos=None, observacoes=None, data_publicacao=None)
    service = SimpleNamespace(criar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(planos_diretores_router, prefix='/urbanismo-habitacao')
    app.dependency_overrides[get_plano_diretor_service] = lambda: service
    client = TestClient(app)
    response = client.post('/urbanismo-habitacao/planos-diretores/', json={'nome': 'Plano Diretor de Luanda 2035', 'tipo': 'municipal', 'provincia': 'Luanda', 'ano_elaboracao': 2026, 'orgao_responsavel_id': str(uuid4()), 'municipio': 'Luanda'})
    assert response.status_code == 201
    assert response.json()['codigo_plano'] == 'PD/2026/000001'

def test_endpoint_obter_plano_diretor_retorna_404():
    service = SimpleNamespace(obter_por_codigo=AsyncMock(side_effect=PlanoDiretorNotFoundError('Plano diretor nao encontrado')))
    app = FastAPI()
    app.include_router(planos_diretores_router, prefix='/urbanismo-habitacao')
    app.dependency_overrides[get_plano_diretor_service] = lambda: service
    client = TestClient(app)
    response = client.get('/urbanismo-habitacao/planos-diretores/PD/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Plano diretor nao encontrado'