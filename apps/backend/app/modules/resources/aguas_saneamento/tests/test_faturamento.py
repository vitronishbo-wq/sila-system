from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.backend.app.modules.resources.aguas_saneamento.api.deps import get_faturamento_service
from apps.backend.app.modules.resources.aguas_saneamento.api.endpoints.faturas import (
    router as faturas_router,
)
from apps.backend.app.modules.resources.aguas_saneamento.application.services.faturamento_service import (
    FaturamentoService,
)
from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import (
    MetodoPagamento,
    StatusFatura,
)
from apps.backend.app.modules.resources.aguas_saneamento.exceptions import FaturaNotFoundError
from apps.backend.app.modules.resources.aguas_saneamento.infrastructure.repositories import (
    SQLAlchemyFaturaRepository,
)


@pytest.mark.asyncio
async def test_faturamento_service_fluxo_sucesso():
    service = FaturamentoService(fatura_repo=SQLAlchemyFaturaRepository())
    item = await service.emitir(
        consumo_id=uuid4(),
        titular_id=uuid4(),
        referencia="2026-03",
        volume_m3=Decimal("18.75"),
        tarifa_m3=Decimal("45.50"),
        data_vencimento=date.today() + timedelta(days=10),
    )
    assert item.status == StatusFatura.EMITIDA
    assert item.valor_total == Decimal("853.12")
    item = await service.registrar_pagamento(
        item.numero_fatura,
        data_pagamento=date.today(),
        valor_pago=item.valor_total,
        metodo_pagamento=MetodoPagamento.MULTICAIXA,
    )
    assert item.status == StatusFatura.PAGA
    assert item.metodo_pagamento == MetodoPagamento.MULTICAIXA


def test_endpoint_emitir_fatura_retorna_201():
    mock_item = SimpleNamespace(
        id=uuid4(),
        numero_fatura="FAT/2026/000001",
        consumo_id=uuid4(),
        titular_id=uuid4(),
        referencia="2026-03",
        volume_m3=Decimal("18.75"),
        tarifa_m3=Decimal("45.50"),
        valor_total=Decimal("853.12"),
        status=StatusFatura.EMITIDA,
        data_emissao=date(2026, 3, 1),
        data_vencimento=date(2026, 3, 10),
        data_pagamento=None,
        valor_pago=None,
        metodo_pagamento=None,
        observacoes=None,
    )
    service = SimpleNamespace(emitir=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(faturas_router, prefix="/aguas-saneamento")
    app.dependency_overrides[get_faturamento_service] = lambda: service
    client = TestClient(app)
    response = client.post(
        "/aguas-saneamento/faturas/",
        json={
            "consumo_id": str(uuid4()),
            "titular_id": str(uuid4()),
            "referencia": "2026-03",
            "volume_m3": "18.75",
            "tarifa_m3": "45.50",
            "data_vencimento": "2026-03-10",
        },
    )
    assert response.status_code == 201
    assert response.json()["numero_fatura"] == "FAT/2026/000001"


def test_endpoint_obter_fatura_retorna_404():
    service = SimpleNamespace(
        obter_por_numero=AsyncMock(side_effect=FaturaNotFoundError("Fatura nao encontrada"))
    )
    app = FastAPI()
    app.include_router(faturas_router, prefix="/aguas-saneamento")
    app.dependency_overrides[get_faturamento_service] = lambda: service
    client = TestClient(app)
    response = client.get("/aguas-saneamento/faturas/FAT/2026/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Fatura nao encontrada"
