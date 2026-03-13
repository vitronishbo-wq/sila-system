from __future__ import annotations
from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.infrastructure_sector.gestao_fundiaria.api.deps import get_desapropriacao_service
from app.modules.infrastructure_sector.gestao_fundiaria.api.endpoints.desapropriacoes import router as desapropriacoes_router
from app.modules.infrastructure_sector.gestao_fundiaria.application.services.desapropriacao_service import DesapropriacaoService
from app.modules.infrastructure_sector.gestao_fundiaria.application.services.imovel_service import ImovelService
from app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import NaturezaImovel, StatusDesapropriacao, TipoDesapropriacao, TipoImovel
from app.modules.infrastructure_sector.gestao_fundiaria.exceptions import DesapropriacaoNotFoundError
from app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.repositories import SQLAlchemyDesapropriacaoRepository, SQLAlchemyImovelRepository

class _AmbienteValido:

    async def validar_car(self, _imovel_id):
        return True

@pytest.mark.asyncio
async def test_desapropriacao_service_fluxo_sucesso() -> None:
    imovel_repo = SQLAlchemyImovelRepository()
    imovel_service = ImovelService(imovel_repo=imovel_repo)
    service = DesapropriacaoService(desapropriacao_repo=SQLAlchemyDesapropriacaoRepository(), imovel_repo=imovel_repo, ambiente_adapter=_AmbienteValido())
    imovel = await imovel_service.cadastrar(tipo=TipoImovel.RURAL, natureza=NaturezaImovel.PRIVADO, area_total=Decimal('2000.00'), endereco='Estrada 100', bairro='Periferia', municipio='Huambo', provincia='Huambo')
    processo = await service.instaurar(imovel_inscricao=imovel.inscricao_imobiliaria, tipo=TipoDesapropriacao.REFORMA_AGRARIA, ente_publico='MINAGRIF', finalidade='Projeto de reforma', valor_indenizacao=Decimal('200000.00'))
    assert processo.status == StatusDesapropriacao.INSTAURADA
    processo = await service.decretar(processo.numero_processo, data_decreto=date.today())
    assert processo.status == StatusDesapropriacao.DECRETADA
    processo = await service.registrar_pagamento(processo.numero_processo)
    assert processo.status == StatusDesapropriacao.INDENIZADA

def test_endpoint_instaurar_desapropriacao_retorna_201() -> None:
    mock_item = SimpleNamespace(id='060b40bf-0842-4329-aeec-7ea7b4f6ea27', numero_processo='DSP/2026/000001', imovel_inscricao='IMV/2026/000010', tipo=TipoDesapropriacao.UTILIDADE_PUBLICA, ente_publico='Governo Provincial', finalidade='Construir hospital', valor_indenizacao=Decimal('500000.00'), data_inicio=date(2026, 3, 4), status=StatusDesapropriacao.INSTAURADA, ativo=True, data_decreto=None, data_pagamento=None, data_atualizacao=None, observacoes=None)
    service = SimpleNamespace(has_ambiente_adapter=lambda: True, instaurar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(desapropriacoes_router, prefix='/gestao-fundiaria')
    app.dependency_overrides[get_desapropriacao_service] = lambda: service
    client = TestClient(app)
    response = client.post('/gestao-fundiaria/desapropriacoes/', json={'imovel_inscricao': 'IMV/2026/000010', 'tipo': 'utilidade_publica', 'ente_publico': 'Governo Provincial', 'finalidade': 'Construir hospital', 'valor_indenizacao': '500000.00'})
    assert response.status_code == 201
    assert response.json()['numero_processo'] == 'DSP/2026/000001'

def test_endpoint_reforma_agraria_sem_adapter_retorna_503() -> None:
    service = SimpleNamespace(has_ambiente_adapter=lambda: False, instaurar=AsyncMock())
    app = FastAPI()
    app.include_router(desapropriacoes_router, prefix='/gestao-fundiaria')
    app.dependency_overrides[get_desapropriacao_service] = lambda: service
    client = TestClient(app)
    response = client.post('/gestao-fundiaria/desapropriacoes/', json={'imovel_inscricao': 'IMV/2026/000010', 'tipo': 'reforma_agraria', 'ente_publico': 'MINAGRIF', 'finalidade': 'Reforma', 'valor_indenizacao': '500000.00'})
    assert response.status_code == 503
    assert 'Adapter de Ambiente indisponivel' in response.json()['detail']
    service.instaurar.assert_not_awaited()

def test_endpoint_obter_desapropriacao_retorna_404() -> None:
    service = SimpleNamespace(obter_por_numero_processo=AsyncMock(side_effect=DesapropriacaoNotFoundError('Desapropriacao nao encontrada')))
    app = FastAPI()
    app.include_router(desapropriacoes_router, prefix='/gestao-fundiaria')
    app.dependency_overrides[get_desapropriacao_service] = lambda: service
    client = TestClient(app)
    response = client.get('/gestao-fundiaria/desapropriacoes/DSP/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Desapropriacao nao encontrada'