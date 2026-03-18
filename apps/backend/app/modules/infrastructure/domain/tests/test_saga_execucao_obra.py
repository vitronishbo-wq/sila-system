from __future__ import annotations
from dataclasses import dataclass, field
import pytest
from apps.backend.app.modules.infrastructure.application.sagas.execucao_obra_saga import ExecucaoObraSaga, ExecucaoObraStates

@dataclass
class _SagaRow:
    saga_type: str
    correlation_id: str
    tenant_id: str
    state: str
    data: dict = field(default_factory=dict)
    completed_at: object | None = None
    updated_at: object | None = None

class _FakeSagaRepo:

    def __init__(self) -> None:
        self.row: _SagaRow | None = None

    async def get_by_correlation(self, session, *, saga_type: str, correlation_id: str, tenant_id: str | None=None):
        _ = (session, saga_type, correlation_id, tenant_id)
        return self.row

    async def create_if_absent(self, session, *, saga_type: str, correlation_id: str, tenant_id: str, state: str, data: dict):
        _ = session
        self.row = _SagaRow(saga_type=saga_type, correlation_id=correlation_id, tenant_id=tenant_id, state=state, data=data)
        return self.row

    async def update_state(self, session, *, row, state: str, data: dict, completed: bool=False):
        _ = session
        row.state = state
        row.data = data
        if completed:
            row.completed_at = object()
        return row

@pytest.mark.asyncio
async def test_execucao_obra_saga_persisted_state_machine():
    repo = _FakeSagaRepo()
    saga = ExecucaoObraSaga(repo)
    session = object()
    await saga.advance(session, event_type='ObraIniciadaEvent', payload={'obra_id': 'obra-1', 'codigo_obra': 'OBR/1'}, correlation_id='corr-1', tenant_id='tenant-1')
    assert repo.row is not None
    assert repo.row.state == ExecucaoObraStates.INICIADA
    await saga.advance(session, event_type='MedicaoAprovadaEvent', payload={'obra_id': 'obra-1', 'codigo_obra': 'OBR/1'}, correlation_id='corr-1', tenant_id='tenant-1')
    assert repo.row.state == ExecucaoObraStates.EMPENHO_GERADO
    await saga.advance(session, event_type='AditivoAssinadoEvent', payload={'obra_id': 'obra-1', 'codigo_obra': 'OBR/1'}, correlation_id='corr-1', tenant_id='tenant-1')
    assert repo.row.state == ExecucaoObraStates.TCU_NOTIFICADO
    result = await saga.advance(session, event_type='ObraConcluidaEvent', payload={'obra_id': 'obra-1', 'codigo_obra': 'OBR/1'}, correlation_id='corr-1', tenant_id='tenant-1')
    assert repo.row.state == ExecucaoObraStates.FINALIZADA
    assert result.completed is True