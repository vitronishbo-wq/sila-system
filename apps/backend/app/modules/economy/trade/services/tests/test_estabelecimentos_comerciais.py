from __future__ import annotations
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.backend.app.modules.economy.trade.services.api.deps import get_estabelecimento_comercial_service
from apps.backend.app.modules.economy.trade.services.api.endpoints.estabelecimentos_comerciais import router as estabelecimentos_router
from apps.backend.app.modules.economy.trade.services.application.services import EstabelecimentoComercialService
from apps.backend.app.modules.economy.trade.services.domain.enums import PorteComercial, RamoComercial, StatusComercial, TipoEstabelecimentoComercial, TipoRegimeTributario
from apps.backend.app.modules.economy.trade.services.domain.models import EstabelecimentoComercial
from apps.backend.app.modules.economy.trade.services.exceptions import EstabelecimentoComercialAlreadyExistsError, EstabelecimentoComercialNotFoundError
from apps.backend.app.modules.economy.trade.services.infrastructure.repositories import SQLAlchemyEstabelecimentoComercialRepository

@pytest.mark.asyncio
async def test_service_fluxo_principal_estabelecimento_comercial():
    service = EstabelecimentoComercialService(repository=SQLAlchemyEstabelecimentoComercialRepository())
    item = await service.cadastrar(cnpj='50020030000199', razao_social='Comercial Luanda Centro SA', tipo=TipoEstabelecimentoComercial.LOJA, ramo=RamoComercial.VAREJISTA, porte=PorteComercial.MEDIA, regime_tributario=TipoRegimeTributario.SIMPLES_NACIONAL, cnae_principal='4711-3/02', data_abertura=date(2026, 1, 10), endereco='Av. Comercio', numero='100', bairro='Centro', municipio='Luanda', provincia='Luanda', cep='1000-001')
    assert item.status == StatusComercial.LICENCIAMENTO
    item = await service.iniciar_atividades(item.id, data_inicio=date(2026, 3, 1))
    assert item.status == StatusComercial.ATIVO
    assert item.audit_log
    before_updated_at = item.updated_at
    item = await service.associar_ramo(item.id, ramo=RamoComercial.ELETRONICOS)
    assert item.ramo == RamoComercial.ELETRONICOS
    assert item.updated_at >= before_updated_at
    before_updated_at = item.updated_at
    item = await service.definir_porte(item.id, porte=PorteComercial.GRANDE)
    assert item.porte == PorteComercial.GRANDE
    assert item.updated_at >= before_updated_at
    assert any(('Ramo associado' in entry for entry in item.audit_log))
    assert any(('Porte definido' in entry for entry in item.audit_log))
    item = await service.suspender_atividades(item.id, motivo='Inventario anual')
    assert item.status == StatusComercial.SUSPENSO
    item = await service.encerrar(item.id, data_encerramento=date(2026, 12, 1), motivo='Encerramento de operacao')
    assert item.status == StatusComercial.INATIVO

@pytest.mark.asyncio
async def test_service_detecta_cnpj_duplicado():
    service = EstabelecimentoComercialService(repository=SQLAlchemyEstabelecimentoComercialRepository())
    payload = dict(cnpj='50020030000188', razao_social='Atacado Benguela SA', tipo=TipoEstabelecimentoComercial.MATRIZ, ramo=RamoComercial.ATACADISTA, porte=PorteComercial.GRANDE, regime_tributario=TipoRegimeTributario.LUCRO_REAL, cnae_principal='4639-7/01', data_abertura=date(2026, 2, 1), endereco='Zona Portuaria', numero='20', bairro='Industrial', municipio='Lobito', provincia='Benguela', cep='2000-100')
    await service.cadastrar(**payload)
    with pytest.raises(EstabelecimentoComercialAlreadyExistsError):
        await service.cadastrar(**payload)

def test_endpoint_cadastrar_retorna_201():
    item = EstabelecimentoComercial.cadastrar(cnpj='50020030000177', razao_social='Loja Huambo SA', tipo=TipoEstabelecimentoComercial.LOJA, ramo=RamoComercial.VESTUARIO, porte=PorteComercial.PEQUENA, regime_tributario=TipoRegimeTributario.SIMPLES_NACIONAL, cnae_principal='4781-4/00', data_abertura=date(2026, 2, 15), endereco='Rua do Mercado', numero='8', bairro='Cidade Alta', municipio='Huambo', provincia='Huambo', cep='3000-200')
    service = SimpleNamespace(cadastrar=AsyncMock(return_value=item))
    app = FastAPI()
    app.include_router(estabelecimentos_router, prefix='/comercio_servicos')
    app.dependency_overrides[get_estabelecimento_comercial_service] = lambda: service
    client = TestClient(app)
    response = client.post('/comercio_servicos/estabelecimentos_comerciais/', json={'cnpj': item.cnpj, 'razao_social': item.razao_social, 'tipo': 'loja', 'ramo': 'vestuario', 'porte': 'pequena', 'regime_tributario': 'simples_nacional', 'cnae_principal': '4781-4/00', 'data_abertura': '2026-02-15', 'endereco': 'Rua do Mercado', 'numero': '8', 'bairro': 'Cidade Alta', 'municipio': 'Huambo', 'provincia': 'Huambo', 'cep': '3000-200'})
    assert response.status_code == 201
    assert response.json()['status'] == 'licenciamento'

def test_endpoint_obter_por_id_retorna_404():
    service = SimpleNamespace(obter_por_id=AsyncMock(side_effect=EstabelecimentoComercialNotFoundError('Estabelecimento comercial nao encontrado')))
    app = FastAPI()
    app.include_router(estabelecimentos_router, prefix='/comercio_servicos')
    app.dependency_overrides[get_estabelecimento_comercial_service] = lambda: service
    client = TestClient(app)
    response = client.get(f'/comercio_servicos/estabelecimentos_comerciais/{uuid4()}')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Estabelecimento comercial nao encontrado'

def test_http_full_cycle_estabelecimento_comercial():
    service = EstabelecimentoComercialService(repository=SQLAlchemyEstabelecimentoComercialRepository())
    app = FastAPI()
    app.include_router(estabelecimentos_router, prefix='/comercio_servicos')
    app.dependency_overrides[get_estabelecimento_comercial_service] = lambda: service
    client = TestClient(app)
    create_resp = client.post('/comercio_servicos/estabelecimentos_comerciais/', json={'cnpj': '50020030000166', 'razao_social': 'Mercado Sul SA', 'tipo': 'matriz', 'ramo': 'supermercado', 'porte': 'grande', 'regime_tributario': 'lucro_presumido', 'cnae_principal': '4711-3/01', 'data_abertura': '2026-01-20', 'endereco': 'Estrada Nacional', 'numero': '150', 'bairro': 'Comercial Sul', 'municipio': 'Lubango', 'provincia': 'Huila', 'cep': '4000-300'})
    assert create_resp.status_code == 201
    item_id = create_resp.json()['id']
    iniciar_resp = client.patch(f'/comercio_servicos/estabelecimentos_comerciais/{item_id}/iniciar_atividades', json={'data': '2026-03-01'})
    assert iniciar_resp.status_code == 200
    assert iniciar_resp.json()['status'] == 'ativo'
    ramo_resp = client.patch(f'/comercio_servicos/estabelecimentos_comerciais/{item_id}/associar_ramo', json={'ramo': 'eletronicos'})
    assert ramo_resp.status_code == 200
    assert ramo_resp.json()['ramo'] == 'eletronicos'
    porte_resp = client.patch(f'/comercio_servicos/estabelecimentos_comerciais/{item_id}/definir_porte', json={'porte': 'emporio'})
    assert porte_resp.status_code == 200
    assert porte_resp.json()['porte'] == 'emporio'
    assert len(porte_resp.json()['audit_log']) > 0
    listar_resp = client.get('/comercio_servicos/estabelecimentos_comerciais/')
    assert listar_resp.status_code == 200
    itens = listar_resp.json()
    assert any((item['id'] == item_id and item['status'] == 'ativo' and (item['ramo'] == 'eletronicos') and (item['porte'] == 'emporio') for item in itens))

def test_http_auditoria_mantem_sequencia_eventos():
    service = EstabelecimentoComercialService(repository=SQLAlchemyEstabelecimentoComercialRepository())
    app = FastAPI()
    app.include_router(estabelecimentos_router, prefix='/comercio_servicos')
    app.dependency_overrides[get_estabelecimento_comercial_service] = lambda: service
    client = TestClient(app)
    create_resp = client.post('/comercio_servicos/estabelecimentos_comerciais/', json={'cnpj': '50020030000155', 'razao_social': 'Loja Eletronica Centro SA', 'tipo': 'loja', 'ramo': 'varejista', 'porte': 'pequena', 'regime_tributario': 'simples_nacional', 'cnae_principal': '4751-2/01', 'data_abertura': '2026-01-05', 'endereco': 'Rua Central', 'numero': '5', 'bairro': 'Centro Comercial', 'municipio': 'Luanda', 'provincia': 'Luanda', 'cep': '1000-010'})
    assert create_resp.status_code == 201
    item_id = create_resp.json()['id']
    assert client.patch(f'/comercio_servicos/estabelecimentos_comerciais/{item_id}/iniciar_atividades', json={'data': '2026-03-10'}).status_code == 200
    assert client.patch(f'/comercio_servicos/estabelecimentos_comerciais/{item_id}/associar_ramo', json={'ramo': 'eletronicos'}).status_code == 200
    assert client.patch(f'/comercio_servicos/estabelecimentos_comerciais/{item_id}/definir_porte', json={'porte': 'media'}).status_code == 200
    assert client.patch(f'/comercio_servicos/estabelecimentos_comerciais/{item_id}/suspender_atividades', json={'motivo': 'Parada tecnica'}).status_code == 200
    assert client.patch(f'/comercio_servicos/estabelecimentos_comerciais/{item_id}/encerrar', json={'data_encerramento': '2026-12-20', 'motivo': 'Encerramento definitivo'}).status_code == 200
    item_resp = client.get(f'/comercio_servicos/estabelecimentos_comerciais/{item_id}')
    assert item_resp.status_code == 200
    audit_log = item_resp.json()['audit_log']
    expected_markers = ['Cadastro inicial do estabelecimento comercial', 'Transicao de status: licenciamento -> ativo', 'Ramo associado:', 'Porte definido:', 'Transicao de status: ativo -> suspenso', 'Transicao de status: -> inativo']
    current_index = 0
    for marker in expected_markers:
        while current_index < len(audit_log) and marker not in audit_log[current_index]:
            current_index += 1
        assert current_index < len(audit_log), f'Evento ausente ou fora de ordem: {marker}'
        current_index += 1