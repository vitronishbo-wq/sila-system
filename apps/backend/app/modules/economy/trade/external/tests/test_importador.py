from __future__ import annotations
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.economy.trade.external.api.deps import get_importador_service
from apps.backend.app.modules.economy.trade.external.api.endpoints.importador import router as importadores_router
from apps.backend.app.modules.economy.trade.external.application.services import ImportadorService
from apps.backend.app.modules.economy.trade.external.domain.enums import RegimeImportacao, StatusHabilitacao, TipoPessoa
from apps.backend.app.modules.economy.trade.external.exceptions import ImportadorAlreadyExistsError, ImportadorNotFoundError
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories import InMemoryImportadorRepository

@pytest.mark.asyncio
async def test_service_fluxo_principal_importador():
    service = ImportadorService(repository=InMemoryImportadorRepository())
    item = await service.cadastrar(razao_social='Import Angola SA', cnpj_cpf='50020030000159', tipo_pessoa=TipoPessoa.JURIDICA, endereco='Av. Alfandega', numero='120', bairro='Centro', municipio='Luanda', provincia='Luanda', cep='1000-010', regimes_autorizados=[RegimeImportacao.DEFINITIVA])
    assert item.status == StatusHabilitacao.PENDENTE
    item = await service.habilitar(item.id, numero_radar='RADAR-2026-2001', data_habilitacao=date(2026, 3, 2), data_validade=date(2027, 3, 2))
    assert item.status == StatusHabilitacao.HABILITADO
    assert item.cadastro_radar == 'RADAR-2026-2001'
    item = await service.adicionar_produto(item.id, produto='Medicamentos')
    item = await service.adicionar_pais_origem(item.id, pais='pt')
    assert item.produtos_principais == ['Medicamentos']
    assert item.paises_origem == ['PT']
    item = await service.suspender(item.id, data_suspensao=date(2026, 7, 1), motivo='Auditoria de compliance')
    assert item.status == StatusHabilitacao.SUSPENSO
    item = await service.reabilitar(item.id)
    assert item.status == StatusHabilitacao.HABILITADO
    item = await service.cancelar(item.id, data_cancelamento=date(2026, 12, 5), motivo='Encerramento da atividade')
    assert item.status == StatusHabilitacao.CANCELADO

@pytest.mark.asyncio
async def test_service_detecta_cnpj_cpf_duplicado_importador():
    service = ImportadorService(repository=InMemoryImportadorRepository())
    payload = dict(razao_social='Duplicado Import SA', cnpj_cpf='50020030000158', tipo_pessoa=TipoPessoa.JURIDICA, endereco='Rua B', numero='2', bairro='Centro', municipio='Luanda', provincia='Luanda', cep='1000-101', regimes_autorizados=[RegimeImportacao.DEFINITIVA])
    await service.cadastrar(**payload)
    with pytest.raises(ImportadorAlreadyExistsError):
        await service.cadastrar(**payload)

def test_endpoint_cadastrar_importador_retorna_201():
    repository = InMemoryImportadorRepository()
    service = ImportadorService(repository=repository)
    app = FastAPI()
    app.include_router(importadores_router, prefix='/comercio_externo')
    app.dependency_overrides[get_importador_service] = lambda: service
    client = TestClient(app)
    response = client.post('/comercio_externo/importadores/', json={'razao_social': 'Import Teste SA', 'cnpj_cpf': '50020030000157', 'tipo_pessoa': 'juridica', 'endereco': 'Rua Porto', 'numero': '15', 'bairro': 'Portuario', 'municipio': 'Lobito', 'provincia': 'Benguela', 'cep': '2000-500', 'regimes_autorizados': ['definitiva', 'temporaria']})
    assert response.status_code == 201
    assert response.json()['status'] == 'pendente'

def test_endpoint_obter_importador_retorna_404():
    service = SimpleNamespace(obter_por_id=AsyncMock(side_effect=ImportadorNotFoundError('Importador nao encontrado')))
    app = FastAPI()
    app.include_router(importadores_router, prefix='/comercio_externo')
    app.dependency_overrides[get_importador_service] = lambda: service
    client = TestClient(app)
    response = client.get(f'/comercio_externo/importadores/{uuid4()}')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Importador nao encontrado'