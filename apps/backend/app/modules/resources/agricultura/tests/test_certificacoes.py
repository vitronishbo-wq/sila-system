from __future__ import annotations
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.resources.agricultura.api.deps import get_certificacao_service
from app.modules.resources.agricultura.api.endpoints.certificacoes import router as certificacoes_router
from app.modules.resources.agricultura.application.services.certificacao_service import CertificacaoService
from app.modules.resources.agricultura.application.services.propriedade_service import PropriedadeService
from app.modules.resources.agricultura.domain.enums import StatusCertificacao, TipoPropriedade
from app.modules.resources.agricultura.exceptions import CertificacaoNotFoundError

@pytest.mark.asyncio
async def test_certificacao_service_fluxo_solicitar_aprovar():
    propriedade_service = PropriedadeService()
    prop = await propriedade_service.cadastrar(produtor_id=uuid4(), nome='Fazenda Sul', tipo=TipoPropriedade.PROPRIO, area_total_ha=120, area_cultivavel_ha=95)
    service = CertificacaoService(propriedade_service=propriedade_service)
    cert = await service.solicitar(codigo_propriedade=prop.codigo_propriedade, tipo='boas_praticas', orgao_emissor='MINAGRIP')
    assert cert.status == StatusCertificacao.SOLICITADA
    cert = await service.aprovar(cert.codigo_certificacao, data_validade=date(2027, 12, 31))
    assert cert.status == StatusCertificacao.APROVADA
    assert cert.data_validade == date(2027, 12, 31)

def test_endpoint_solicitar_certificacao_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), codigo_certificacao='CER/2026/000001', codigo_propriedade='PROP/2026/000001', tipo='boas_praticas', orgao_emissor='MINAGRIP', status='solicitada', data_solicitacao='2026-02-28', data_emissao=None, data_validade=None, motivo_reprovacao=None)
    service = SimpleNamespace(solicitar=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(certificacoes_router, prefix='/agricultura')
    app.dependency_overrides[get_certificacao_service] = lambda: service
    client = TestClient(app)
    response = client.post('/agricultura/certificacoes/', json={'codigo_propriedade': 'PROP/2026/000001', 'tipo': 'boas_praticas', 'orgao_emissor': 'MINAGRIP'})
    assert response.status_code == 201
    assert response.json()['codigo_certificacao'] == 'CER/2026/000001'

def test_endpoint_obter_certificacao_retorna_404():
    service = SimpleNamespace(obter=AsyncMock(side_effect=CertificacaoNotFoundError('Certificacao nao encontrada')))
    app = FastAPI()
    app.include_router(certificacoes_router, prefix='/agricultura')
    app.dependency_overrides[get_certificacao_service] = lambda: service
    client = TestClient(app)
    response = client.get('/agricultura/certificacoes/CER/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Certificacao nao encontrada'