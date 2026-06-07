from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.backend.app.modules.infrastructure.api.deps import get_licitacao_service
from apps.backend.app.modules.infrastructure.api.endpoints.licitacoes import (
    router as licitacoes_router,
)
from apps.backend.app.modules.infrastructure.application.services.licitacao_service import (
    LicitacaoService,
)
from apps.backend.app.modules.infrastructure.domain.enums import StatusLicitacao, TipoLicitacao
from apps.backend.app.modules.infrastructure.domain.exceptions import LicitacaoNotFoundError
from apps.backend.app.modules.infrastructure.infrastructure.repositories import (
    SQLAlchemyLicitacaoRepository,
)


@pytest.mark.asyncio
async def test_licitacao_service_fluxo_sucesso():
    service = LicitacaoService(licitacao_repo=SQLAlchemyLicitacaoRepository())
    item = await service.abrir(
        objeto="Contratacao para pavimentacao da via X",
        tipo=TipoLicitacao.CONCORRENCIA,
        obra_id=uuid4(),
        orgao_responsavel_id=uuid4(),
        valor_estimado=Decimal("1200000.00"),
        data_publicacao_edital=date.today(),
        data_entrega_propostas=date.today() + timedelta(days=15),
    )
    assert item.status == StatusLicitacao.EDITAL_PUBLICADO
    assert item.numero_licitacao.startswith("LIC/")
    item = await service.iniciar_recebimento(item.numero_licitacao)
    assert item.status == StatusLicitacao.RECEBENDO_PROPOSTAS
    item = await service.encerrar_recebimento(
        item.numero_licitacao, data_abertura=date.today() + timedelta(days=15)
    )
    assert item.status == StatusLicitacao.PROPOSTAS_ENTREGUES
    item = await service.iniciar_analise(item.numero_licitacao)
    assert item.status == StatusLicitacao.EM_ANALISE
    item = await service.abrir_habilitacao(item.numero_licitacao)
    assert item.status == StatusLicitacao.HABILITACAO
    item = await service.adjudicar(
        item.numero_licitacao, vencedor_id=uuid4(), valor_adjudicado=Decimal("1180000.00")
    )
    assert item.status == StatusLicitacao.ADJUDICADA
    item = await service.homologar(item.numero_licitacao)
    assert item.status == StatusLicitacao.HOMOLOGADA


def test_endpoint_abrir_licitacao_retorna_201():
    mock_item = SimpleNamespace(
        id=uuid4(),
        numero_licitacao="LIC/2026/000001",
        objeto="Contratacao para pavimentacao da via X",
        tipo=TipoLicitacao.CONCORRENCIA,
        status=StatusLicitacao.EDITAL_PUBLICADO,
        obra_id=uuid4(),
        orgao_responsavel_id=uuid4(),
        valor_estimado=Decimal("1200000.00"),
        data_publicacao_edital=date(2026, 3, 1),
        data_entrega_propostas=date(2026, 3, 16),
        data_cadastro=date(2026, 3, 1),
        data_abertura=None,
        vencedor_id=None,
        valor_adjudicado=None,
        data_homologacao=None,
        data_atualizacao=None,
        observacoes=None,
    )
    service = SimpleNamespace(abrir=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(licitacoes_router, prefix="/obras-publicas")
    app.dependency_overrides[get_licitacao_service] = lambda: service
    client = TestClient(app)
    response = client.post(
        "/obras-publicas/licitacoes/",
        json={
            "objeto": "Contratacao para pavimentacao da via X",
            "tipo": "concorrencia",
            "obra_id": str(uuid4()),
            "orgao_responsavel_id": str(uuid4()),
            "valor_estimado": "1200000.00",
            "data_publicacao_edital": "2026-03-01",
            "data_entrega_propostas": "2026-03-16",
        },
    )
    assert response.status_code == 201
    assert response.json()["numero_licitacao"] == "LIC/2026/000001"


def test_endpoint_obter_licitacao_retorna_404():
    service = SimpleNamespace(
        obter_por_numero=AsyncMock(side_effect=LicitacaoNotFoundError("Licitacao nao encontrada"))
    )
    app = FastAPI()
    app.include_router(licitacoes_router, prefix="/obras-publicas")
    app.dependency_overrides[get_licitacao_service] = lambda: service
    client = TestClient(app)
    response = client.get("/obras-publicas/licitacoes/LIC/2026/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Licitacao nao encontrada"
