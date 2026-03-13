from __future__ import annotations
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.industry.api.deps import get_estabelecimento_industrial_service
from app.modules.industry.api.endpoints.estabelecimentos_industriais import router as estabelecimentos_router
from app.modules.industry.application.services import EstabelecimentoIndustrialService
from app.modules.industry.domain.enums import PorteIndustrial, RamoIndustrial, StatusEstabelecimento, TipoEstabelecimento
from app.modules.industry.domain.models import EstabelecimentoIndustrial
from app.modules.industry.core.exceptions import EstabelecimentoIndustrialAlreadyExistsError, EstabelecimentoIndustrialNotFoundError
from app.modules.industry.infrastructure.repositories import SQLAlchemyEstabelecimentoIndustrialRepository

@pytest.mark.asyncio
async def test_service_fluxo_principal_estabelecimento():
    service = EstabelecimentoIndustrialService(repository=SQLAlchemyEstabelecimentoIndustrialRepository())
    item = await service.cadastrar(cnpj='50010020000199', razao_social='Fabrica Luanda Norte SA', ramo=RamoIndustrial.TRANSFORMACAO, porte=PorteIndustrial.MEDIA, tipo=TipoEstabelecimento.MATRIZ, cnae_principal='1031-7/00', data_abertura=date(2026, 1, 1), endereco='Av. Principal 100', bairro='Benfica', municipio='Luanda', provincia='Luanda')
    assert item.status == StatusEstabelecimento.LICENCIAMENTO
    item = await service.iniciar_atividades(item.id, data_inicio=date(2026, 3, 1))
    assert item.status == StatusEstabelecimento.ATIVO
    assert item.audit_log
    before_updated_at = item.updated_at
    item = await service.associar_ramo(item.id, ramo=RamoIndustrial.QUIMICA)
    assert item.ramo == RamoIndustrial.QUIMICA
    assert item.updated_at >= before_updated_at
    before_updated_at = item.updated_at
    item = await service.definir_porte(item.id, porte=PorteIndustrial.GRANDE)
    assert item.porte == PorteIndustrial.GRANDE
    assert item.updated_at >= before_updated_at
    assert any(('Ramo associado' in entry for entry in item.audit_log))
    assert any(('Porte definido' in entry for entry in item.audit_log))
    item = await service.suspender_atividades(item.id, motivo='Manutencao anual')
    assert item.status == StatusEstabelecimento.SUSPENSO
    item = await service.reativar(item.id)
    assert item.status == StatusEstabelecimento.ATIVO

@pytest.mark.asyncio
async def test_service_detecta_cnpj_duplicado():
    service = EstabelecimentoIndustrialService(repository=SQLAlchemyEstabelecimentoIndustrialRepository())
    payload = dict(cnpj='50010020000188', razao_social='Metalurgica Benguela SA', ramo=RamoIndustrial.METALURGICA, porte=PorteIndustrial.GRANDE, tipo=TipoEstabelecimento.MATRIZ, cnae_principal='2599-3/01', data_abertura=date(2026, 2, 1), endereco='Zona Industrial A, lote 4', bairro='Centro', municipio='Lobito', provincia='Benguela')
    await service.cadastrar(**payload)
    with pytest.raises(EstabelecimentoIndustrialAlreadyExistsError):
        await service.cadastrar(**payload)

def test_endpoint_cadastrar_retorna_201():
    item = EstabelecimentoIndustrial.cadastrar(cnpj='50010020000177', razao_social='Textil Huambo SA', ramo=RamoIndustrial.TEXTIL, porte=PorteIndustrial.PEQUENA, tipo=TipoEstabelecimento.FILIAL, cnae_principal='1311-1/00', data_abertura=date(2026, 2, 15), endereco='Rua das Industrias, 10', bairro='Cidade Alta', municipio='Huambo', provincia='Huambo')
    service = SimpleNamespace(cadastrar=AsyncMock(return_value=item))
    app = FastAPI()
    app.include_router(estabelecimentos_router, prefix='/industria')
    app.dependency_overrides[get_estabelecimento_industrial_service] = lambda: service
    client = TestClient(app)
    response = client.post('/industria/estabelecimentos_industriais/', json={'cnpj': item.cnpj, 'razao_social': item.razao_social, 'ramo': 'textil', 'porte': 'pequena', 'tipo': 'filial', 'cnae_principal': '1311-1/00', 'data_abertura': '2026-02-15', 'endereco': 'Rua das Industrias, 10', 'bairro': 'Cidade Alta', 'municipio': 'Huambo', 'provincia': 'Huambo'})
    assert response.status_code == 201
    assert response.json()['status'] == 'licenciamento'

def test_endpoint_obter_por_id_retorna_404():
    service = SimpleNamespace(obter_por_id=AsyncMock(side_effect=EstabelecimentoIndustrialNotFoundError('Estabelecimento industrial nao encontrado')))
    app = FastAPI()
    app.include_router(estabelecimentos_router, prefix='/industria')
    app.dependency_overrides[get_estabelecimento_industrial_service] = lambda: service
    client = TestClient(app)
    response = client.get(f'/industria/estabelecimentos_industriais/{uuid4()}')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Estabelecimento industrial nao encontrado'

def test_http_full_cycle_estabelecimento_industrial():
    service = EstabelecimentoIndustrialService(repository=SQLAlchemyEstabelecimentoIndustrialRepository())
    app = FastAPI()
    app.include_router(estabelecimentos_router, prefix='/industria')
    app.dependency_overrides[get_estabelecimento_industrial_service] = lambda: service
    client = TestClient(app)
    create_resp = client.post('/industria/estabelecimentos_industriais/', json={'cnpj': '50010020000166', 'razao_social': 'Alimentos Sul SA', 'ramo': 'alimentar', 'porte': 'media', 'tipo': 'matriz', 'cnae_principal': '1099-6/01', 'data_abertura': '2026-01-20', 'endereco': 'Estrada Nacional KM 12', 'bairro': 'Industrial Sul', 'municipio': 'Lubango', 'provincia': 'Huila'})
    assert create_resp.status_code == 201
    item_id = create_resp.json()['id']
    iniciar_resp = client.patch(f'/industria/estabelecimentos_industriais/{item_id}/iniciar_atividades', json={'data': '2026-03-01'})
    assert iniciar_resp.status_code == 200
    assert iniciar_resp.json()['status'] == 'ativo'
    ramo_resp = client.patch(f'/industria/estabelecimentos_industriais/{item_id}/associar_ramo', json={'ramo': 'quimica'})
    assert ramo_resp.status_code == 200
    assert ramo_resp.json()['ramo'] == 'quimica'
    assert len(ramo_resp.json()['audit_log']) > 0
    porte_resp = client.patch(f'/industria/estabelecimentos_industriais/{item_id}/definir_porte', json={'porte': 'grande'})
    assert porte_resp.status_code == 200
    assert porte_resp.json()['porte'] == 'grande'
    assert len(porte_resp.json()['audit_log']) > 0
    listar_resp = client.get('/industria/estabelecimentos_industriais/')
    assert listar_resp.status_code == 200
    itens = listar_resp.json()
    assert any((item['id'] == item_id and item['status'] == 'ativo' and (item['ramo'] == 'quimica') and (item['porte'] == 'grande') for item in itens))

def test_http_auditoria_mantem_sequencia_eventos():
    service = EstabelecimentoIndustrialService(repository=SQLAlchemyEstabelecimentoIndustrialRepository())
    app = FastAPI()
    app.include_router(estabelecimentos_router, prefix='/industria')
    app.dependency_overrides[get_estabelecimento_industrial_service] = lambda: service
    client = TestClient(app)
    create_resp = client.post('/industria/estabelecimentos_industriais/', json={'cnpj': '50010020000155', 'razao_social': 'Quimica Centro SA', 'ramo': 'transformacao', 'porte': 'pequena', 'tipo': 'matriz', 'cnae_principal': '2013-4/00', 'data_abertura': '2026-01-05', 'endereco': 'Rua 5, lote 8', 'bairro': 'Centro Industrial', 'municipio': 'Luanda', 'provincia': 'Luanda'})
    assert create_resp.status_code == 201
    item_id = create_resp.json()['id']
    assert client.patch(f'/industria/estabelecimentos_industriais/{item_id}/iniciar_atividades', json={'data': '2026-03-10'}).status_code == 200
    assert client.patch(f'/industria/estabelecimentos_industriais/{item_id}/associar_ramo', json={'ramo': 'quimica'}).status_code == 200
    assert client.patch(f'/industria/estabelecimentos_industriais/{item_id}/definir_porte', json={'porte': 'media'}).status_code == 200
    assert client.patch(f'/industria/estabelecimentos_industriais/{item_id}/suspender_atividades', json={'motivo': 'Parada tecnica'}).status_code == 200
    assert client.patch(f'/industria/estabelecimentos_industriais/{item_id}/reativar').status_code == 200
    item_resp = client.get(f'/industria/estabelecimentos_industriais/{item_id}')
    assert item_resp.status_code == 200
    audit_log = item_resp.json()['audit_log']
    expected_markers = ['Cadastro inicial do estabelecimento industrial', 'Transicao de status: licenciamento -> ativo', 'Ramo associado:', 'Porte definido:', 'Transicao de status: ativo -> suspenso', 'Transicao de status: suspenso/paralisado -> ativo']
    current_index = 0
    for marker in expected_markers:
        while current_index < len(audit_log) and marker not in audit_log[current_index]:
            current_index += 1
        assert current_index < len(audit_log), f'Evento ausente ou fora de ordem: {marker}'
        current_index += 1
