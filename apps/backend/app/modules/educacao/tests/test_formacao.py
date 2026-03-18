from __future__ import annotations
import asyncio
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4
from apps.backend.app.modules.educacao.application.formacao_service import FormacaoService
from apps.backend.app.modules.educacao.domain.enums import StatusFluxo
from apps.backend.app.modules.educacao.domain.models.formacao_profissional import DomainRecord
from apps.backend.app.modules.educacao.domain.models._workflow_record import WorkflowRecord

def test_formacao_domain_transitions():
    item = DomainRecord(id=uuid4(), numero_processo='FRM/2026/0001', service_type='formacao_profissional', citizen_id=uuid4(), instituicao_id=uuid4(), data_registo=date.today())
    item.cancelar('motivo')
    assert item.status == StatusFluxo.CANCELADA

def test_formacao_service_create_and_complete():
    citizen_id = uuid4()
    instituicao_id = uuid4()
    saved = WorkflowRecord(id=uuid4(), numero_processo='FRM/FORMACAO_PROFISSIONAL/2026/0002', service_type='formacao_profissional', citizen_id=citizen_id, instituicao_id=instituicao_id, data_registo=date.today())
    repository = SimpleNamespace(exists_active_for_citizen=AsyncMock(return_value=False), next_numero_processo=AsyncMock(return_value=saved.numero_processo), save=AsyncMock(return_value=saved), get_by_id=AsyncMock(return_value=saved), list_by_citizen=AsyncMock(return_value=[saved]))
    service = FormacaoService(repository=repository, citizen_repo=SimpleNamespace(get_by_id=AsyncMock(return_value=SimpleNamespace(id=citizen_id))), request_service=SimpleNamespace(create_education_request=AsyncMock(return_value=uuid4()), mark_education_request_completed=AsyncMock(return_value=True)))
    asyncio.run(service.create_record(service_type='formacao_profissional', citizen_id=citizen_id, instituicao_id=instituicao_id))
    completed = asyncio.run(service.conclude_record(saved.id, uuid4(), 'ok'))
    assert completed.status == StatusFluxo.CONCLUIDA