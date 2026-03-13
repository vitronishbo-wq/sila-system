from __future__ import annotations
from apps.backend.app.modules.infrastructure.application.eventsourcing.obra_event_aggregate import rehydrate_obra
from apps.backend.app.modules.infrastructure.infrastructure.governance.event_governance import EventGovernanceService
from apps.backend.app.modules.infrastructure.infrastructure.multi_region.global_id import generate_global_id

def test_generate_global_id_com_prefixo_regiao():
    gid = generate_global_id('B')
    assert gid.startswith('B-')
    assert len(gid.split('-')) >= 2

def test_rehydrate_obra_a_partir_de_eventos():
    events = [{'event_type': 'ObraCriadaEvent', 'event_data': {'codigo_obra': 'OBR/2026/000001', 'valor_orcado': '1000.00'}}, {'event_type': 'ObraIniciadaEvent', 'event_data': {'data_inicio': '2026-03-01'}}, {'event_type': 'MedicaoAprovadaEvent', 'event_data': {'valor_medido': '250.00'}}]
    state = rehydrate_obra('obra-1', events)
    assert state.codigo_obra == 'OBR/2026/000001'
    assert state.status == 'EM_EXECUCAO'
    assert str(state.valor_total) == '1000.00'
    assert str(state.valor_executado) == '250.00'

def test_contract_registry_tem_eventos_obrigatorios():
    governance = EventGovernanceService()
    contract = governance.resolve_contract('ObraIniciadaEvent')
    assert contract.version == 1
    assert contract.owner == 'MINOPUH'
    assert contract.schema['type'] == 'record'
