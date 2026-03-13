from __future__ import annotations
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.resources.pescas.api.deps import get_licenciamento_pesca_service
from app.modules.resources.pescas.api.endpoints.licencas_pesca import router as licencas_router
from app.modules.resources.pescas.application.services.licenciamento_pesca_service import LicenciamentoPescaService
from app.modules.resources.pescas.domain.enums import StatusLicenca
from app.modules.resources.pescas.domain.models.licenca_pesca import LicencaPesca

@pytest.mark.asyncio
async def test_emitir_licenca_sucesso():
    embarcacao_id = uuid4()
    titular_id = uuid4()
    zona_id = uuid4()
    embarcacao_repo = SimpleNamespace(get_by_id=AsyncMock(return_value={'id': embarcacao_id}))
    licenca_repo = SimpleNamespace(next_numero=AsyncMock(return_value='LIC/2026/000001'), save=AsyncMock(side_effect=lambda i: i))
    service = LicenciamentoPescaService(licenca_repo=licenca_repo, embarcacao_repo=embarcacao_repo)
    result = await service.emitir_licenca(embarcacao_id=embarcacao_id, titular_id=titular_id, modalidade_autorizada='arrasto', zona_pesca_id=zona_id)
    assert result.numero_licenca == 'LIC/2026/000001'
    assert result.status == StatusLicenca.DEFERIDA

def test_endpoint_listar_licencas_ok():
    item = LicencaPesca.emitir(numero_licenca='LIC/2026/000001', embarcacao_id=uuid4(), titular_id=uuid4(), data_emissao=date.today(), data_validade=date.today(), modalidade_autorizada='arrasto', zona_pesca_id=uuid4())
    service = SimpleNamespace(listar_licencas_validas=AsyncMock(return_value=[item]))
    app = FastAPI()
    app.include_router(licencas_router, prefix='/pescas')
    app.dependency_overrides[get_licenciamento_pesca_service] = lambda: service
    client = TestClient(app)
    response = client.get('/pescas/licencas-pesca/')
    assert response.status_code == 200
    assert response.json()[0]['numero_licenca'] == 'LIC/2026/000001'