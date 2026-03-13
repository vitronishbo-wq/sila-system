from __future__ import annotations
from datetime import date, datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from app.modules.justice.bounded_contexts.infrastructure.adapters.saude_service_adapter import SaudeServiceAdapter

@pytest.mark.asyncio
async def test_adapter_saude_retorna_resumo_do_ultimo_registro() -> None:
    citizen_id = uuid4()
    antigo = SimpleNamespace(id=uuid4(), record_number='MR-001', diagnosis=['hipertensao'], follow_up_date=date(2026, 3, 10), created_at=datetime(2026, 2, 1), updated_at=datetime(2026, 2, 1))
    recente = SimpleNamespace(id=uuid4(), record_number='MR-002', diagnosis=['asma'], follow_up_date=date(2026, 4, 10), created_at=datetime(2026, 3, 1), updated_at=datetime(2026, 3, 2))
    repo = SimpleNamespace(get_by_citizen=AsyncMock(side_effect=[[antigo, recente], [antigo]]))
    adapter = SaudeServiceAdapter(repo)
    resumo = await adapter.get_resumo_saude(citizen_id)
    possui = await adapter.has_registro_medico(citizen_id)
    assert resumo is not None
    assert resumo['total_registros'] == 2
    assert resumo['ultimo_numero'] == 'MR-002'
    assert possui is True