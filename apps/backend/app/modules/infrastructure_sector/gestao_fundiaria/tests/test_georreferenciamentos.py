from __future__ import annotations

from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.api.deps import (
    get_georreferenciamento_service,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.api.endpoints.georreferenciamentos import (
    router as georreferenciamentos_router,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.services.georreferenciamento_service import (
    GeorreferenciamentoService,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.services.imovel_service import (
    ImovelService,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import (
    NaturezaImovel,
    TipoImovel,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.exceptions import (
    GeorreferenciamentoNotFoundError,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.repositories import (
    SQLAlchemyGeorreferenciamentoRepository,
    SQLAlchemyImovelRepository,
)


class _GeosampaValido:
    async def validar_coordenadas(self, latitude: Decimal, longitude: Decimal) -> bool:
        _ = (latitude, longitude)
        return True


@pytest.mark.asyncio
async def test_georreferenciamento_service_fluxo_sucesso() -> None:
    imovel_repo = SQLAlchemyImovelRepository()
    imovel_service = ImovelService(imovel_repo=imovel_repo)
    service = GeorreferenciamentoService(
        georreferenciamento_repo=SQLAlchemyGeorreferenciamentoRepository(),
        imovel_repo=imovel_repo,
        geosampa_adapter=_GeosampaValido(),
    )
    imovel = await imovel_service.cadastrar(
        tipo=TipoImovel.RURAL,
        natureza=NaturezaImovel.PRIVADO,
        area_total=Decimal("2000.00"),
        endereco="Estrada do Campo, 50",
        bairro="Zona Rural",
        municipio="Kuito",
        provincia="Bie",
    )
    geo = await service.registrar(
        imovel_inscricao=imovel.inscricao_imobiliaria,
        latitude=Decimal("-12.12345678"),
        longitude=Decimal("15.12345678"),
        precisao_metros=Decimal("2.50"),
        area_calculada=Decimal("2000.50"),
    )
    assert geo.codigo_geo.startswith("GEO/")
    assert geo.validado is True
    geo = await service.atualizar_ponto(
        geo.codigo_geo, latitude=Decimal("-12.12345000"), longitude=Decimal("15.12345000")
    )
    assert geo.latitude == Decimal("-12.12345000")
    assert geo.longitude == Decimal("15.12345000")
    linked_imovel = await imovel_repo.get_by_inscricao(imovel.inscricao_imobiliaria)
    assert linked_imovel is not None
    assert linked_imovel.coordenadas_lat == Decimal("-12.12345000")
    assert linked_imovel.coordenadas_long == Decimal("15.12345000")


def test_endpoint_registrar_georreferenciamento_retorna_201() -> None:
    mock_item = SimpleNamespace(
        id=uuid4(),
        codigo_geo="GEO/2026/000001",
        imovel_inscricao="IMV/2026/000001",
        latitude=Decimal("-12.12345678"),
        longitude=Decimal("15.12345678"),
        sistema_referencia="WGS84",
        data_registro=date(2026, 3, 4),
        precisao_metros=Decimal("1.50"),
        area_calculada=Decimal("450.00"),
        validado=True,
        ativo=True,
        data_atualizacao=None,
        observacoes=None,
    )
    service = SimpleNamespace(
        has_geosampa_adapter=lambda: True, registrar=AsyncMock(return_value=mock_item)
    )
    app = FastAPI()
    app.include_router(georreferenciamentos_router, prefix="/gestao-fundiaria")
    app.dependency_overrides[get_georreferenciamento_service] = lambda: service
    client = TestClient(app)
    response = client.post(
        "/gestao-fundiaria/georreferenciamentos/",
        json={
            "imovel_inscricao": "IMV/2026/000001",
            "latitude": "-12.12345678",
            "longitude": "15.12345678",
            "sistema_referencia": "WGS84",
            "precisao_metros": "1.50",
            "area_calculada": "450.00",
        },
    )
    assert response.status_code == 201
    assert response.json()["codigo_geo"] == "GEO/2026/000001"


def test_endpoint_registrar_georreferenciamento_sem_adapter_retorna_503() -> None:
    service = SimpleNamespace(has_geosampa_adapter=lambda: False, registrar=AsyncMock())
    app = FastAPI()
    app.include_router(georreferenciamentos_router, prefix="/gestao-fundiaria")
    app.dependency_overrides[get_georreferenciamento_service] = lambda: service
    client = TestClient(app)
    response = client.post(
        "/gestao-fundiaria/georreferenciamentos/",
        json={
            "imovel_inscricao": "IMV/2026/000001",
            "latitude": "-12.12345678",
            "longitude": "15.12345678",
        },
    )
    assert response.status_code == 503
    assert "Adapter de Geosampa indisponivel" in response.json()["detail"]
    service.registrar.assert_not_awaited()


def test_endpoint_obter_georreferenciamento_retorna_404() -> None:
    service = SimpleNamespace(
        obter_por_codigo=AsyncMock(
            side_effect=GeorreferenciamentoNotFoundError("Georreferenciamento nao encontrado")
        )
    )
    app = FastAPI()
    app.include_router(georreferenciamentos_router, prefix="/gestao-fundiaria")
    app.dependency_overrides[get_georreferenciamento_service] = lambda: service
    client = TestClient(app)
    response = client.get("/gestao-fundiaria/georreferenciamentos/GEO/2026/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Georreferenciamento nao encontrado"
