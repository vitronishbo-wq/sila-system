from __future__ import annotations
from decimal import Decimal
import pytest
from apps.backend.app.modules.infrastructure.infrastructure.read_model.dashboard_projection_repository import DashboardProjectionRepository

class _FakeSession:

    def __init__(self) -> None:
        self.rows: dict[str, object] = {}

    async def get(self, model, key):
        _ = model
        return self.rows.get(key)

    def add(self, row):
        self.rows[row.obra_id] = row

    async def flush(self):
        return None

@pytest.mark.asyncio
async def test_dashboard_projection_obra_criada_e_medicao():
    repo = DashboardProjectionRepository()
    session = _FakeSession()
    await repo.project(session, event_type='ObraCriadaEvent', payload={'obra_id': 'obra-1', 'codigo_obra': 'OBR/2026/000001', 'valor_orcado': '1000.00'}, tenant_id='tenant-1')
    row = session.rows['obra-1']
    assert Decimal(str(row.valor_total)) == Decimal('1000.00')
    assert Decimal(str(row.valor_executado)) == Decimal('0.00')
    await repo.project(session, event_type='MedicaoAprovadaEvent', payload={'obra_id': 'obra-1', 'codigo_obra': 'OBR/2026/000001', 'valor_medido': '250.00'}, tenant_id='tenant-1')
    assert Decimal(str(row.valor_executado)) == Decimal('250.00')
    assert Decimal(str(row.percentual_execucao)).quantize(Decimal('0.01')) == Decimal('25.00')