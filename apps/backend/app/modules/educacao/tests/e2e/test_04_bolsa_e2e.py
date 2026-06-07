"""E2E: Bolsa — Pagamento + workflow + eventos.

Fluxo:
  BolsaService.create_record()
    → Workflow steps (analise → aprovacao → pagamento → concedida)
    → PagamentoMatriculaService.confirmar_pagamento()
    → EventBus.publish(BolsaCandidaturaSubmetida)
    → AuditLogger.log()
"""

from __future__ import annotations

from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from apps.backend.app.modules.educacao.application.workflow_service import WorkflowService
from apps.backend.app.modules.educacao.domain.enums import StatusFluxo
from apps.backend.app.modules.educacao.domain.models._workflow_record import WorkflowRecord
from sila_platform.governance.audit.logger import AuditLogger, AuditAction


@pytest.mark.asyncio
async def test_bolsa_fluxo_completo_com_pagamento_e_eventos(
    mock_event_bus, mock_educacao_service_port
):
    citizen_id = uuid4()
    bolsa_id = uuid4()

    saved = WorkflowRecord(
        id=bolsa_id,
        numero_processo="BOL/E2E/2026/0001",
        service_type="bolsa",
        citizen_id=citizen_id,
        instituicao_id=uuid4(),
        data_registo=date.today(),
    )

    repository = SimpleNamespace(
        exists_active_for_citizen=AsyncMock(return_value=False),
        next_numero_processo=AsyncMock(return_value=saved.numero_processo),
        save=AsyncMock(return_value=saved),
        get_by_id=AsyncMock(return_value=saved),
        list_by_citizen=AsyncMock(return_value=[saved]),
    )
    citizen_repo = SimpleNamespace(
        get_by_id=AsyncMock(return_value=SimpleNamespace(id=citizen_id))
    )
    request_service = SimpleNamespace(
        create_education_request=AsyncMock(return_value=uuid4()),
        mark_education_request_completed=AsyncMock(return_value=True),
    )

    service = WorkflowService(
        repository=repository,
        process_prefix="BOL",
        citizen_repo=citizen_repo,
        request_service=request_service,
    )
    audit = AuditLogger()

    # ── Step 1: Criar candidatura a bolsa ────────────────────────────
    record = await service.create_record(
        service_type="bolsa_candidatura",
        citizen_id=citizen_id,
        instituicao_id=uuid4(),
        observacoes="Candidatura E2E",
    )
    assert record is not None
    assert record.numero_processo == "BOL/E2E/2026/0001"

    audit.log(
        actor_id=str(citizen_id),
        actor_role="operador",
        action=AuditAction.CREATE,
        resource_type="bolsa",
        resource_id=str(bolsa_id),
        module="educacao",
        details={"numero_processo": record.numero_processo},
    )

    # ── Step 2: Simular pagamento via PagamentoMatriculaService ──────
    from apps.backend.app.modules.educacao.application.pagamento_matricula_service import (
        PagamentoMatriculaService,
    )

    pag_svc = PagamentoMatriculaService(
        educacao_service_port=mock_educacao_service_port,
        event_bus=mock_event_bus,
    )
    ref = await pag_svc.gerar_referencia(
        wizard_id=bolsa_id,
        citizen_id=citizen_id,
        amount=50000.0,
    )
    assert ref is not None
    assert ref.amount == 50000.0

    await pag_svc.confirmar_pagamento(
        wizard_id=bolsa_id,
        citizen_id=citizen_id,
        payment_ref=ref.reference,
        amount=50000.0,
    )

    audit.log(
        actor_id=str(citizen_id),
        actor_role="operador",
        action=AuditAction.UPDATE,
        resource_type="bolsa_pagamento",
        resource_id=ref.reference,
        module="educacao",
        details={"amount": 50000.0, "status": "CONFIRMADO"},
    )

    # ── Step 3: Concluir bolsa ──────────────────────────────────────
    saved.confirmar()
    saved.concluir("concedida")
    assert saved.status == StatusFluxo.CONCLUIDA

    audit.log(
        actor_id=str(citizen_id),
        actor_role="nacional",
        action=AuditAction.UPDATE,
        resource_type="bolsa",
        resource_id=str(bolsa_id),
        module="educacao",
        details={"status": "concedida"},
    )

    # ── Step 4: Verificar eventos publicados ─────────────────────────
    published = mock_event_bus.get_published()
    payment_events = [e for e in published if e.event_type == "PaymentConfirmed"]
    assert len(payment_events) >= 1

    port_calls = mock_educacao_service_port.get_calls()
    assert len(port_calls) >= 2  # gerar_referencia + confirmar_pagamento

    # ── Step 5: Verificar auditoria ─────────────────────────────────
    assert len(audit._entries) == 3  # CREATE + UPDATE(pagamento) + UPDATE(concedida)

    print(f"E2E Bolsa OK — eventos={len(published)}, audit={len(audit._entries)}, pagamentos={len(port_calls)}")


@pytest.mark.asyncio
async def test_bolsa_cancelamento():
    citizen_id = uuid4()
    bolsa_id = uuid4()

    saved = WorkflowRecord(
        id=bolsa_id,
        numero_processo="BOL/E2E/2026/0002",
        service_type="bolsa",
        citizen_id=citizen_id,
        instituicao_id=uuid4(),
        data_registo=date.today(),
    )

    repository = SimpleNamespace(
        exists_active_for_citizen=AsyncMock(return_value=False),
        next_numero_processo=AsyncMock(return_value=saved.numero_processo),
        save=AsyncMock(return_value=saved),
        get_by_id=AsyncMock(return_value=saved),
    )
    citizen_repo = SimpleNamespace(
        get_by_id=AsyncMock(return_value=SimpleNamespace(id=citizen_id))
    )
    request_service = SimpleNamespace(
        create_education_request=AsyncMock(return_value=uuid4()),
        mark_education_request_completed=AsyncMock(return_value=True),
    )

    service = WorkflowService(
        repository=repository,
        process_prefix="BOL",
        citizen_repo=citizen_repo,
        request_service=request_service,
    )

    await service.create_record(
        service_type="bolsa_candidatura",
        citizen_id=citizen_id,
        instituicao_id=uuid4(),
    )

    cancelled = await service.cancel_record(
        record_id=bolsa_id,
        actor_id=citizen_id,
        motivo="Desistencia do candidato",
    )
    assert cancelled is not None
    assert saved.status == StatusFluxo.CANCELADA
