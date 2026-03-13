from __future__ import annotations
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.modules.resources.agricultura.api.deps import get_operacao_service
from app.modules.resources.agricultura.api.endpoints.operacoes import router as operacoes_router
from app.modules.resources.agricultura.application.services.insumo_service import InsumoService
from app.modules.resources.agricultura.application.services.operacao_service import OperacaoService
from app.modules.resources.agricultura.application.services.producao_service import ProducaoService
from app.modules.resources.agricultura.application.services.propriedade_service import PropriedadeService
from app.modules.resources.agricultura.application.services.safra_service import SafraService
from app.modules.resources.agricultura.domain.enums import TipoCultura, TipoInsumo, TipoOperacao, TipoPropriedade
from app.modules.resources.agricultura.exceptions import OperacaoNotFoundError

@pytest.mark.asyncio
async def test_operacao_service_registrar_com_consumo_insumo():
    propriedade_service = PropriedadeService()
    producao_service = ProducaoService()
    safra_service = SafraService(propriedade_service=propriedade_service, producao_service=producao_service)
    insumo_service = InsumoService()
    prop = await propriedade_service.cadastrar(produtor_id=uuid4(), nome='Fazenda Norte', tipo=TipoPropriedade.PROPRIO, area_total_ha=90, area_cultivavel_ha=70)
    cultura = await producao_service.cadastrar_cultura(nome='Feijao', tipo=TipoCultura.GRAOS, ciclo_dias=110, produtividade_estimada_ton_ha=2.1)
    safra = await safra_service.criar_safra(codigo_propriedade=prop.codigo_propriedade, codigo_cultura=cultura.codigo_cultura, ano=2026, area_plantada_ha=35, producao_estimada_ton=60)
    insumo = await insumo_service.cadastrar(nome='Semente Feijao', tipo=TipoInsumo.SEMENTE, unidade_medida='kg', quantidade_inicial=100, custo_unitario=8)
    service = OperacaoService(safra_service=safra_service, insumo_service=insumo_service)
    op = await service.registrar_operacao(codigo_safra=safra.codigo_safra, tipo=TipoOperacao.PLANTIO, descricao='Plantio inicial', codigo_insumo=insumo.codigo_insumo, quantidade_insumo=25)
    atualizado = await insumo_service.obter(insumo.codigo_insumo)
    assert op.codigo_operacao.startswith('OPE/')
    assert atualizado.quantidade_estoque == 75

def test_endpoint_registrar_operacao_retorna_201():
    mock_item = SimpleNamespace(id=uuid4(), codigo_operacao='OPE/2026/000001', codigo_safra='SAF/2026/000001', tipo='plantio', descricao='Plantio inicial', data_operacao='2026-02-28T00:00:00', codigo_insumo='INS/2026/000001', quantidade_insumo=12.0)
    service = SimpleNamespace(registrar_operacao=AsyncMock(return_value=mock_item))
    app = FastAPI()
    app.include_router(operacoes_router, prefix='/agricultura')
    app.dependency_overrides[get_operacao_service] = lambda: service
    client = TestClient(app)
    response = client.post('/agricultura/operacoes/', json={'codigo_safra': 'SAF/2026/000001', 'tipo': 'plantio', 'descricao': 'Plantio inicial', 'codigo_insumo': 'INS/2026/000001', 'quantidade_insumo': 12})
    assert response.status_code == 201
    assert response.json()['codigo_operacao'] == 'OPE/2026/000001'

def test_endpoint_obter_operacao_retorna_404():
    service = SimpleNamespace(obter=AsyncMock(side_effect=OperacaoNotFoundError('Operacao nao encontrada')))
    app = FastAPI()
    app.include_router(operacoes_router, prefix='/agricultura')
    app.dependency_overrides[get_operacao_service] = lambda: service
    client = TestClient(app)
    response = client.get('/agricultura/operacoes/OPE/2026/999999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Operacao nao encontrada'