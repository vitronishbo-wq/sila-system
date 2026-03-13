from __future__ import annotations
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.resources.agricultura.api.deps import get_zoneamento_service
from app.modules.resources.agricultura.api.endpoints.zoneamento import router as zoneamento_router
from app.modules.resources.agricultura.application.services.propriedade_service import PropriedadeService
from app.modules.resources.agricultura.application.services.zoneamento_service import ZoneamentoService
from app.modules.resources.agricultura.domain.enums import AptidaoSolo, StatusCadastroAmbiental, StatusZoneamento, TipoPropriedade, TipoZonaAgricola
from app.modules.resources.agricultura.exceptions import ZoneamentoNotFoundError

@pytest.mark.asyncio
async def test_zoneamento_service_fluxo_completo_cadastro_ambiental():
    propriedade_service = PropriedadeService()
    prop = await propriedade_service.cadastrar(produtor_id=uuid4(), nome='Fazenda Centro', tipo=TipoPropriedade.PROPRIO, area_total_ha=70, area_cultivavel_ha=48)
    service = ZoneamentoService(propriedade_service=propriedade_service)
    zoneamento = await service.registrar_zoneamento(codigo_propriedade=prop.codigo_propriedade, zona=TipoZonaAgricola.USO_MISTO, aptidao_solo=AptidaoSolo.MEDIA, area_zoneada_ha=45, culturas_recomendadas=['milho', 'feijao'])
    assert zoneamento.status == StatusZoneamento.ATIVO
    cadastro = await service.registrar_cadastro_ambiental(codigo_zoneamento=zoneamento.codigo_zoneamento, reserva_legal_percentual=20, app_percentual=12, area_protecao_ha=9)
    assert cadastro.status == StatusCadastroAmbiental.PENDENTE
    cadastro = await service.registrar_pendencia(cadastro.codigo_cadastro_ambiental, pendencia='Falta memorial descritivo')
    assert cadastro.status == StatusCadastroAmbiental.COM_PENDENCIA
    with pytest.raises(ValueError):
        await service.validar_cadastro(cadastro.codigo_cadastro_ambiental, numero_processo='PROC-123')
    cadastro = await service.sanar_pendencias(cadastro.codigo_cadastro_ambiental)
    assert cadastro.status == StatusCadastroAmbiental.PENDENTE
    cadastro = await service.validar_cadastro(cadastro.codigo_cadastro_ambiental, numero_processo='PROC-123')
    assert cadastro.status == StatusCadastroAmbiental.VALIDADO

def test_endpoint_registrar_zoneamento_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), codigo_zoneamento='ZON/2026/000001', codigo_propriedade='PROP/2026/000001', zona=TipoZonaAgricola.USO_MISTO, aptidao_solo=AptidaoSolo.MEDIA, area_zoneada_ha=45.0, status=StatusZoneamento.ATIVO, data_zoneamento=date(2026, 2, 28), culturas_recomendadas=['milho', 'feijao'], restricoes=[], validade_ate=None, observacoes=None)
    service = SimpleNamespace(registrar_zoneamento=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(zoneamento_router, prefix='/agricultura')
    app.dependency_overrides[get_zoneamento_service] = lambda: service
    client = TestClient(app)
    response = client.post('/agricultura/zoneamento/', json={'codigo_propriedade': 'PROP/2026/000001', 'zona': 'uso_misto', 'aptidao_solo': 'media', 'area_zoneada_ha': 45, 'culturas_recomendadas': ['milho', 'feijao']})
    assert response.status_code == 201
    assert response.json()['codigo_zoneamento'] == 'ZON/2026/000001'

def test_endpoint_obter_zoneamento_retorna_404():
    service = SimpleNamespace(obter_zoneamento=AsyncMock(side_effect=ZoneamentoNotFoundError('Zoneamento nao encontrado')))
    app = FastAPI()
    app.include_router(zoneamento_router, prefix='/agricultura')
    app.dependency_overrides[get_zoneamento_service] = lambda: service
    client = TestClient(app)
    response = client.get('/agricultura/zoneamento/ZON/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Zoneamento nao encontrado'

def test_endpoint_registrar_cadastro_ambiental_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), codigo_cadastro_ambiental='CAR/2026/000001', codigo_zoneamento='ZON/2026/000001', codigo_propriedade='PROP/2026/000001', reserva_legal_percentual=20.0, app_percentual=12.0, area_protecao_ha=9.0, status=StatusCadastroAmbiental.PENDENTE, data_registro=date(2026, 2, 28), numero_processo=None, data_validacao=None, pendencias=[])
    service = SimpleNamespace(registrar_cadastro_ambiental=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(zoneamento_router, prefix='/agricultura')
    app.dependency_overrides[get_zoneamento_service] = lambda: service
    client = TestClient(app)
    response = client.post('/agricultura/zoneamento/ZON/2026/000001/cadastro-ambiental', json={'reserva_legal_percentual': 20, 'app_percentual': 12, 'area_protecao_ha': 9})
    assert response.status_code == 201
    assert response.json()['codigo_cadastro_ambiental'] == 'CAR/2026/000001'