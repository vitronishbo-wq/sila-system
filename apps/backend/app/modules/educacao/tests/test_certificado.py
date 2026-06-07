from __future__ import annotations

import asyncio
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

from apps.backend.app.modules.educacao.application.certificado_service import CertificadoService
from apps.backend.app.modules.educacao.domain.enums import StatusFluxo
from apps.backend.app.modules.educacao.domain.models._workflow_record import WorkflowRecord
from apps.backend.app.modules.educacao.domain.models.certificado_conclusao import DomainRecord


def test_certificado_domain_transitions():
    item = DomainRecord(
        id=uuid4(),
        numero_processo="CRT/2026/0001",
        service_type="certificado_conclusao",
        citizen_id=uuid4(),
        instituicao_id=uuid4(),
        data_registo=date.today(),
    )
    item.confirmar()
    item.concluir("emitido")
    assert item.status == StatusFluxo.CONCLUIDA


def test_certificado_service_create_and_complete():
    citizen_id = uuid4()
    instituicao_id = uuid4()
    saved = WorkflowRecord(
        id=uuid4(),
        numero_processo="CRT/CERTIFICADO_CONCLUSAO/2026/0002",
        service_type="certificado_conclusao",
        citizen_id=citizen_id,
        instituicao_id=instituicao_id,
        data_registo=date.today(),
    )
    repository = SimpleNamespace(
        exists_active_for_citizen=AsyncMock(return_value=False),
        next_numero_processo=AsyncMock(return_value=saved.numero_processo),
        save=AsyncMock(return_value=saved),
        get_by_id=AsyncMock(return_value=saved),
        list_by_citizen=AsyncMock(return_value=[saved]),
    )
    citizen_repo = SimpleNamespace(get_by_id=AsyncMock(return_value=SimpleNamespace(id=citizen_id)))
    request_service = SimpleNamespace(
        create_education_request=AsyncMock(return_value=uuid4()),
        mark_education_request_completed=AsyncMock(return_value=True),
    )
    service = CertificadoService(
        repository=repository, citizen_repo=citizen_repo, request_service=request_service
    )
    asyncio.run(
        service.create_record(
            service_type="certificado_conclusao",
            citizen_id=citizen_id,
            instituicao_id=instituicao_id,
        )
    )
    completed = asyncio.run(service.conclude_record(saved.id, uuid4(), "ok"))
    assert completed.status == StatusFluxo.CONCLUIDA
