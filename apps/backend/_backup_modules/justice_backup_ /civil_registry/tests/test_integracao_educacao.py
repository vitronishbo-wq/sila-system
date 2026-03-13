from __future__ import annotations
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest
from app.modules.educacao.infrastructure.models import StatusMatricula
from app.modules.justice.bounded_contexts.application.services.citizen_service import CitizenService
from app.modules.justice.bounded_contexts.infrastructure.adapters.educacao_service_adapter import EducacaoServiceAdapter

@pytest.mark.asyncio
async def test_adapter_educacao_filtra_matriculas_ativas() -> None:
    citizen_id = uuid4()
    repo = SimpleNamespace(get_by_citizen=AsyncMock(return_value=[SimpleNamespace(id=uuid4(), numero_processo='2026/00001', escola_id=uuid4(), turma_id=uuid4(), ano_letivo_id=uuid4(), status=StatusMatricula.ATIVA, data_matricula=date(2026, 3, 1)), SimpleNamespace(id=uuid4(), numero_processo='2026/00002', escola_id=uuid4(), turma_id=uuid4(), ano_letivo_id=uuid4(), status=StatusMatricula.CANCELADA, data_matricula=date(2026, 3, 1))]))
    adapter = EducacaoServiceAdapter(repo)
    matriculas = await adapter.get_matriculas_ativas(citizen_id)
    tem_ativa = await adapter.has_matricula_ativa(citizen_id)
    assert len(matriculas) == 1
    assert matriculas[0]['status'] == StatusMatricula.ATIVA.value
    assert tem_ativa is True

@pytest.mark.asyncio
async def test_citizen_service_enriquece_com_educacao() -> None:
    citizen_id = str(uuid4())
    query_service = SimpleNamespace(get_by_fuc_id=AsyncMock(return_value=SimpleNamespace(id=citizen_id, full_name='Joao Silva', birth_date=date(2000, 1, 1), vital_status='alive', documents=[{'type': 'BI', 'number': '123'}])))
    educacao_service = SimpleNamespace(get_matriculas_ativas=AsyncMock(return_value=[{'numero_processo': '2026/00001'}]), has_matricula_ativa=AsyncMock(return_value=True))
    service = CitizenService(query_service=query_service, educacao_service=educacao_service)
    result = await service.get_citizen_completo(citizen_id)
    assert result is not None
    assert result['cidadao']['full_name'] == 'Joao Silva'
    assert result['integracoes']['educacao']['tem_matricula_ativa'] is True