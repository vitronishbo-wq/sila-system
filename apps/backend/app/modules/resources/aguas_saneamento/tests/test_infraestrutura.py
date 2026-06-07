from __future__ import annotations

from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.backend.app.modules.resources.aguas_saneamento.api.deps import get_infraestrutura_service
from apps.backend.app.modules.resources.aguas_saneamento.api.endpoints.infraestrutura import (
    router as infraestrutura_router,
)
from apps.backend.app.modules.resources.aguas_saneamento.application.services.infraestrutura_service import (
    InfraestruturaService,
)
from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import (
    StatusInfraestrutura,
    TipoInfraestrutura,
)
from apps.backend.app.modules.resources.aguas_saneamento.exceptions import (
    InfraestruturaNotFoundError,
)
from apps.backend.app.modules.resources.aguas_saneamento.infrastructure.repositories import (
    SQLAlchemyInfraestruturaRepository,
)


@pytest.mark.asyncio
async def test_infraestrutura_service_fluxo_sucesso():
    service = InfraestruturaService(infraestrutura_repo=SQLAlchemyInfraestruturaRepository())
    infraestrutura = await service.registrar(
        tipo=TipoInfraestrutura.ETA,
        nome="ETA Luanda Sul",
        provincia="Luanda",
        municipio="Belas",
        capacidade=Decimal("2500.00"),
        unidade_capacidade="m3/dia",
    )
    assert infraestrutura.status == StatusInfraestrutura.PLANEJADA
    infraestrutura = await service.ativar(infraestrutura.codigo_infraestrutura)
    assert infraestrutura.status == StatusInfraestrutura.OPERACIONAL
    assert infraestrutura.data_operacao == date.today()
    infraestrutura = await service.manutencao(
        infraestrutura.codigo_infraestrutura, motivo="Manutencao preventiva"
    )
    assert infraestrutura.status == StatusInfraestrutura.MANUTENCAO
    infraestrutura = await service.reativar(
        infraestrutura.codigo_infraestrutura, motivo="Servico concluido"
    )
    assert infraestrutura.status == StatusInfraestrutura.OPERACIONAL
    infraestrutura = await service.desativar(
        infraestrutura.codigo_infraestrutura, motivo="Encerramento operacional"
    )
    assert infraestrutura.status == StatusInfraestrutura.INATIVA


def test_endpoint_registrar_infraestrutura_retorna_201():
    mock_item = SimpleNamespace(
        id=uuid4(),
        codigo_infraestrutura="INF/2026/000001",
        tipo=TipoInfraestrutura.ETA,
        nome="ETA Luanda Sul",
        provincia="Luanda",
        municipio="Belas",
        status=StatusInfraestrutura.PLANEJADA,
        data_registro=date(2026, 3, 1),
        capacidade=Decimal("2500.00"),
        unidade_capacidade="m3/dia",
        outorga_id=None,
        latitude=None,
        longitude=None,
        data_operacao=None,
        observacoes=None,
    )
    service = SimpleNamespace(registrar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(infraestrutura_router, prefix="/aguas-saneamento")
    app.dependency_overrides[get_infraestrutura_service] = lambda: service
    client = TestClient(app)
    response = client.post(
        "/aguas-saneamento/infraestrutura/",
        json={
            "tipo": "eta",
            "nome": "ETA Luanda Sul",
            "provincia": "Luanda",
            "municipio": "Belas",
            "capacidade": "2500.00",
            "unidade_capacidade": "m3/dia",
        },
    )
    assert response.status_code == 201
    assert response.json()["codigo_infraestrutura"] == "INF/2026/000001"


def test_endpoint_obter_infraestrutura_retorna_404():
    service = SimpleNamespace(
        obter_por_codigo=AsyncMock(
            side_effect=InfraestruturaNotFoundError("Infraestrutura nao encontrada")
        )
    )
    app = FastAPI()
    app.include_router(infraestrutura_router, prefix="/aguas-saneamento")
    app.dependency_overrides[get_infraestrutura_service] = lambda: service
    client = TestClient(app)
    response = client.get("/aguas-saneamento/infraestrutura/INF/2026/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Infraestrutura nao encontrada"
