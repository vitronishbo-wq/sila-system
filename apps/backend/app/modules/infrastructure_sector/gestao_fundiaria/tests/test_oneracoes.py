from __future__ import annotations

from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.api.deps import (
    get_oneracao_service,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.api.endpoints.oneracoes import (
    router as oneracoes_router,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.services.imovel_service import (
    ImovelService,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.services.oneracao_service import (
    OneracaoService,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import (
    NaturezaImovel,
    StatusOneracao,
    TipoImovel,
    TipoOneracao,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.exceptions import (
    OneracaoNotFoundError,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.repositories import (
    SQLAlchemyImovelRepository,
    SQLAlchemyOneracaoRepository,
)


class _JusticaComLitigio:
    async def possui_litigio_ativo(self, _imovel_id):
        return True


@pytest.mark.asyncio
async def test_oneracao_service_fluxo_sucesso() -> None:
    imovel_repo = SQLAlchemyImovelRepository()
    imovel_service = ImovelService(imovel_repo=imovel_repo)
    oneracao_service = OneracaoService(
        oneracao_repo=SQLAlchemyOneracaoRepository(),
        imovel_repo=imovel_repo,
        justica_adapter=_JusticaComLitigio(),
    )
    imovel = await imovel_service.cadastrar(
        tipo=TipoImovel.URBANO,
        natureza=NaturezaImovel.PRIVADO,
        area_total=Decimal("300.00"),
        endereco="Rua 1",
        bairro="Centro",
        municipio="Luanda",
        provincia="Luanda",
    )
    item = await oneracao_service.registrar(
        imovel_inscricao=imovel.inscricao_imobiliaria,
        tipo=TipoOneracao.PENHORA,
        credor_nome="Banco Publico",
        valor=Decimal("15000.00"),
    )
    assert item.status == StatusOneracao.ATIVA
    item = await oneracao_service.baixar(item.numero_oneracao, motivo="Quitacao integral")
    assert item.status == StatusOneracao.BAIXADA
    assert item.ativo is False


def test_endpoint_registrar_oneracao_retorna_201() -> None:
    mock_item = SimpleNamespace(
        id="3f2eb5f0-8308-45a5-a357-f6c2d2f8facc",
        numero_oneracao="ONR/2026/000001",
        imovel_inscricao="IMV/2026/000001",
        tipo=TipoOneracao.HIPOTECA,
        credor_nome="Banco X",
        valor=Decimal("1000.00"),
        data_registro=date(2026, 3, 4),
        status=StatusOneracao.ATIVA,
        ativo=True,
        documento_credor=None,
        moeda="AOA",
        data_vencimento=None,
        descricao=None,
        data_atualizacao=None,
        observacoes=None,
    )
    service = SimpleNamespace(
        has_justica_adapter=lambda: True, registrar=AsyncMock(return_value=mock_item)
    )
    app = FastAPI()
    app.include_router(oneracoes_router, prefix="/gestao-fundiaria")
    app.dependency_overrides[get_oneracao_service] = lambda: service
    client = TestClient(app)
    response = client.post(
        "/gestao-fundiaria/oneracoes/",
        json={
            "imovel_inscricao": "IMV/2026/000001",
            "tipo": "hipoteca",
            "credor_nome": "Banco X",
            "valor": "1000.00",
        },
    )
    assert response.status_code == 201
    assert response.json()["numero_oneracao"] == "ONR/2026/000001"


def test_endpoint_penhora_sem_adapter_retorna_503() -> None:
    service = SimpleNamespace(has_justica_adapter=lambda: False, registrar=AsyncMock())
    app = FastAPI()
    app.include_router(oneracoes_router, prefix="/gestao-fundiaria")
    app.dependency_overrides[get_oneracao_service] = lambda: service
    client = TestClient(app)
    response = client.post(
        "/gestao-fundiaria/oneracoes/",
        json={
            "imovel_inscricao": "IMV/2026/000001",
            "tipo": "penhora",
            "credor_nome": "Tribunal",
            "valor": "1000.00",
        },
    )
    assert response.status_code == 503
    assert "Adapter de Justica indisponivel" in response.json()["detail"]
    service.registrar.assert_not_awaited()


def test_endpoint_obter_oneracao_retorna_404() -> None:
    service = SimpleNamespace(
        obter_por_numero=AsyncMock(side_effect=OneracaoNotFoundError("Oneracao nao encontrada"))
    )
    app = FastAPI()
    app.include_router(oneracoes_router, prefix="/gestao-fundiaria")
    app.dependency_overrides[get_oneracao_service] = lambda: service
    client = TestClient(app)
    response = client.get("/gestao-fundiaria/oneracoes/ONR/2026/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Oneracao nao encontrada"
