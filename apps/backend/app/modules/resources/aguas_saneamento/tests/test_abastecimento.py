from __future__ import annotations

from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.backend.app.modules.resources.aguas_saneamento.api.deps import get_abastecimento_service
from apps.backend.app.modules.resources.aguas_saneamento.api.endpoints.abastecimento import (
    router as abastecimento_router,
)
from apps.backend.app.modules.resources.aguas_saneamento.application.services.abastecimento_service import (
    AbastecimentoService,
)
from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import StatusAbastecimento
from apps.backend.app.modules.resources.aguas_saneamento.exceptions import (
    AbastecimentoNotFoundError,
)
from apps.backend.app.modules.resources.aguas_saneamento.infrastructure.repositories import (
    SQLAlchemyAbastecimentoRepository,
)


@pytest.mark.asyncio
async def test_abastecimento_service_fluxo_sucesso():
    service = AbastecimentoService(abastecimento_repo=SQLAlchemyAbastecimentoRepository())
    item = await service.registrar(
        infraestrutura_id=uuid4(),
        nome_sistema="Sistema Central Luanda",
        provincia="Luanda",
        municipio="Talatona",
    )
    assert item.status == StatusAbastecimento.PLANEJADO
    item = await service.iniciar_operacao(item.codigo_abastecimento)
    assert item.status == StatusAbastecimento.OPERACIONAL
    assert item.data_inicio_operacao == date.today()
    item = await service.interromper(item.codigo_abastecimento, motivo="Falha de energia")
    assert item.status == StatusAbastecimento.INTERROMPIDO
    item = await service.retomar(item.codigo_abastecimento)
    assert item.status == StatusAbastecimento.OPERACIONAL
    item = await service.encerrar(item.codigo_abastecimento, motivo="Substituicao de sistema")
    assert item.status == StatusAbastecimento.ENCERRADO


def test_endpoint_registrar_abastecimento_retorna_201():
    mock_item = SimpleNamespace(
        id=uuid4(),
        codigo_abastecimento="ABS/2026/000001",
        infraestrutura_id=uuid4(),
        nome_sistema="Sistema Central Luanda",
        provincia="Luanda",
        municipio="Talatona",
        status=StatusAbastecimento.PLANEJADO,
        data_registro=date(2026, 3, 1),
        data_inicio_operacao=None,
        data_interrupcao=None,
        motivo_interrupcao=None,
        observacoes=None,
    )
    service = SimpleNamespace(registrar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(abastecimento_router, prefix="/aguas-saneamento")
    app.dependency_overrides[get_abastecimento_service] = lambda: service
    client = TestClient(app)
    response = client.post(
        "/aguas-saneamento/abastecimento/",
        json={
            "infraestrutura_id": str(uuid4()),
            "nome_sistema": "Sistema Central Luanda",
            "provincia": "Luanda",
            "municipio": "Talatona",
        },
    )
    assert response.status_code == 201
    assert response.json()["codigo_abastecimento"] == "ABS/2026/000001"


def test_endpoint_obter_abastecimento_retorna_404():
    service = SimpleNamespace(
        obter_por_codigo=AsyncMock(
            side_effect=AbastecimentoNotFoundError("Abastecimento nao encontrado")
        )
    )
    app = FastAPI()
    app.include_router(abastecimento_router, prefix="/aguas-saneamento")
    app.dependency_overrides[get_abastecimento_service] = lambda: service
    client = TestClient(app)
    response = client.get("/aguas-saneamento/abastecimento/ABS/2026/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Abastecimento nao encontrado"
