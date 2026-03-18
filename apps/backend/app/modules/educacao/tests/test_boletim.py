from __future__ import annotations
import asyncio
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
from apps.backend.app.modules.educacao.application.boletim_service import BoletimService
from apps.backend.app.modules.educacao.domain.enums import StatusFluxo
from apps.backend.app.modules.educacao.domain.models.boletim import DomainRecord
from apps.backend.app.modules.educacao.domain.models._workflow_record import WorkflowRecord

def test_boletim_domain_transitions():
    item = DomainRecord(id=uuid4(), numero_processo='BLT/2026/0001', service_type='boletim', citizen_id=uuid4(), instituicao_id=uuid4(), data_registo=date.today())
    assert item.status == StatusFluxo.PENDENTE
    item.confirmar()
    assert item.status == StatusFluxo.CONFIRMADA
    item.concluir('ok')
    assert item.status == StatusFluxo.CONCLUIDA

def test_boletim_service_create_and_complete():
    citizen_id = uuid4()
    instituicao_id = uuid4()
    saved = WorkflowRecord(id=uuid4(), numero_processo='BLT/BOLETIM/2026/0002', service_type='boletim', citizen_id=citizen_id, instituicao_id=instituicao_id, data_registo=date.today())
    repository = SimpleNamespace(exists_active_for_citizen=AsyncMock(return_value=False), next_numero_processo=AsyncMock(return_value=saved.numero_processo), save=AsyncMock(return_value=saved), get_by_id=AsyncMock(return_value=saved), list_by_citizen=AsyncMock(return_value=[saved]))
    citizen_repo = SimpleNamespace(get_by_id=AsyncMock(return_value=SimpleNamespace(id=citizen_id)))
    request_service = SimpleNamespace(create_education_request=AsyncMock(return_value=uuid4()), mark_education_request_completed=AsyncMock(return_value=True))
    service = BoletimService(repository=repository, citizen_repo=citizen_repo, request_service=request_service)
    created = asyncio.run(service.create_record(service_type='boletim', citizen_id=citizen_id, instituicao_id=instituicao_id, observacoes='teste'))
    assert created.id == saved.id
    request_service.create_education_request.assert_awaited_once()
    completed = asyncio.run(service.conclude_record(saved.id, uuid4(), 'finalizado'))
    assert completed.status == StatusFluxo.CONCLUIDA