from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.backend.app.modules.resources.pescas.api.deps import get_captura_service
from apps.backend.app.modules.resources.pescas.api.endpoints.capturas import (
    router as capturas_router,
)
from apps.backend.app.modules.resources.pescas.application.services.captura_service import (
    CapturaService,
)
from apps.backend.app.modules.resources.pescas.domain.enums import StatusLicenca


@pytest.mark.asyncio
async def test_registrar_captura_sucesso():
    licenca = SimpleNamespace(
        status=StatusLicenca.DEFERIDA, data_validade=date.today() + timedelta(days=1)
    )
    licenca_repo = SimpleNamespace(get_by_id=AsyncMock(return_value=licenca))
    captura_repo = SimpleNamespace(save=AsyncMock(side_effect=lambda i: i))
    service = CapturaService(captura_repo=captura_repo, licenca_repo=licenca_repo)
    result = await service.registrar_captura(
        embarcacao_id=uuid4(),
        licenca_id=uuid4(),
        zona_pesca_id=uuid4(),
        especie_id=uuid4(),
        quantidade_kg=Decimal("100.5"),
        arte_pesca_id=uuid4(),
    )
    assert result.quantidade_kg == Decimal("100.5")


def test_endpoint_registrar_captura_400():
    service = SimpleNamespace(
        registrar_captura=AsyncMock(side_effect=ValueError("Licenca vencida"))
    )
    app = FastAPI()
    app.include_router(capturas_router, prefix="/pescas")
    app.dependency_overrides[get_captura_service] = lambda: service
    client = TestClient(app)
    response = client.post(
        "/pescas/capturas/",
        json={
            "embarcacao_id": str(uuid4()),
            "licenca_id": str(uuid4()),
            "zona_pesca_id": str(uuid4()),
            "especie_id": str(uuid4()),
            "quantidade_kg": "10.0",
            "arte_pesca_id": str(uuid4()),
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Licenca vencida"
