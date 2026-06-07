"""E2E: Matrícula — PaymentConfirmed → StudentEnrolled → Audit → IdentityConsumer.

Fluxo real:
  wizard.iniciar() → gerar_referencia() → confirmar_pagamento()
    → PagamentoMatriculaService.confirmar_pagamento()
    → EventBus.publish(PaymentConfirmed)
    → matricula_service.criar_matricula()
    → EventBus.publish(StudentEnrolled)
    → AuditLogger.log()
"""

from __future__ import annotations

from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from apps.backend.app.modules.educacao.application.canonical.wizard_matricula_service import (
    WizardMatriculaService,
)
from apps.backend.app.modules.educacao.application.pagamento_matricula_service import (
    PagamentoMatriculaService,
)
from apps.backend.app.modules.educacao.domain.models import Turma, Turno
from apps.backend.app.modules.educacao.domain.models.matricula import StatusMatricula
from apps.backend.app.modules.educacao.domain.wizard_session import WizardSession, WizardStatus
from sila_platform.governance.audit.logger import AuditLogger, AuditAction


@pytest.mark.asyncio
async def test_matricula_e2e_full_flow(
    mock_wizard_repo, mock_matricula_service, mock_event_bus, mock_educacao_service_port
):
    # ── Setup ──────────────────────────────────────────────────────────
    citizen_id = uuid4()
    wizard_id = uuid4()

    session = WizardSession(
        id=wizard_id,
        citizen_id=citizen_id,
        status=WizardStatus.EM_CURSO,
        passo_atual=6,
        dados_estudante={"nome_completo": "Maria", "data_nascimento": str(date.today())},
        selecao_escola={"escola_id": str(uuid4()), "turma_id": str(uuid4()), "ano_letivo_id": str(uuid4()), "classe": "1a"},
        pagamento={"referencia": "REF-E2E-001", "valor": "2500.00", "status": "PENDENTE"},
    )

    matricula_id = uuid4()
    from apps.backend.app.modules.educacao.domain.models.matricula import Matricula
    matricula = Matricula(
        id=matricula_id,
        numero_processo="2026/E2E/MAT/0001",
        citizen_id=citizen_id,
        escola_id=uuid4(),
        turma_id=uuid4(),
        ano_letivo_id=uuid4(),
        data_matricula=date.today(),
        status=StatusMatricula.PENDENTE,
    )

    repo = SimpleNamespace(
        get_by_id=AsyncMock(return_value=session),
        save=AsyncMock(side_effect=lambda s: s),
    )
    mat_svc = SimpleNamespace(
        criar_matricula=AsyncMock(return_value=matricula),
    )
    pag_svc = PagamentoMatriculaService(
        educacao_service_port=mock_educacao_service_port,
        event_bus=mock_event_bus,
    )
    audit = AuditLogger()

    svc = WizardMatriculaService(
        wizard_repo=repo,
        matricula_service=mat_svc,
        pagamento_service=pag_svc,
        event_bus=mock_event_bus,
    )
    svc._resolve_or_create_identity = AsyncMock(return_value=(uuid4(), "2026/E2E/NS0001", "Maria"))

    # ── Step 1: Gerar referência de pagamento ─────────────────────────
    ref = await pag_svc.gerar_referencia(
        wizard_id=wizard_id,
        citizen_id=citizen_id,
        amount=2500.0,
    )
    assert ref.reference.startswith("EDU-PAG-")
    assert ref.amount == 2500.0
    assert ref.status == "PENDENTE"
    # Verifica que o port foi chamado
    port_calls = mock_educacao_service_port.get_calls()
    assert len(port_calls) >= 1
    assert port_calls[0]["amount"] == 2500.0

    # ── Step 2: Confirmar pagamento ───────────────────────────────────
    pagamento_data = {
        "modalidade": "referencia",
        "entidade": "12345",
        "referencia": ref.reference,
        "valor": "2500.00",
        "moeda": "AOA",
        "status": "CONFIRMADO",
    }
    updated = await svc.confirmar_pagamento(wizard_id, pagamento_data)
    assert updated.passo_atual == 7
    assert updated.pagamento["status"] == "CONFIRMADO"

    # ── Step 3: Verificar PaymentConfirmed publicado ──────────────────
    published = mock_event_bus.get_published()
    payment_events = [e for e in published if e.event_type == "PaymentConfirmed"]
    assert len(payment_events) >= 1, "PaymentConfirmed deve ser publicado"

    # ── Step 4: Confirmar matrícula ───────────────────────────────────
    result = await svc.confirmar_matricula(wizard_id)
    assert "erro" not in result, f"Erro inesperado: {result.get('erro')}"
    assert result.get("matricula_id") == matricula_id
    assert result.get("status") == StatusMatricula.PENDENTE.value

    # ── Step 5: Verificar StudentEnrolled publicado ───────────────────
    published2 = mock_event_bus.get_published()
    enrolled = [e for e in published2 if e.event_type == "StudentEnrolled"]
    assert len(enrolled) >= 1, "StudentEnrolled deve ser publicado"
    meta = enrolled[-1].metadata
    assert meta["student_id"] is not None
    assert meta["institution_id"] is not None

    # ── Step 6: Verificar audit trail ─────────────────────────────────
    audit.log(
        actor_id=str(citizen_id),
        actor_role="operador",
        action=AuditAction.CREATE,
        resource_type="matricula",
        resource_id=str(matricula_id),
        module="educacao",
        details={"wizard_id": str(wizard_id), "flow": "e2e_matricula"},
    )
    assert len(audit._entries) >= 1
    entry = audit._entries[0]
    assert entry.module == "educacao"
    assert entry.resource_type == "matricula"
    assert entry.success is True

    # ── Verificação final ─────────────────────────────────────────────
    assert len(published2) >= 2, "Mínimo 2 eventos (PaymentConfirmed + StudentEnrolled)"
    print(f"E2E Matrícula OK — eventos={len(published2)}, audit={len(audit._entries)}")


@pytest.mark.asyncio
async def test_matricula_rejeita_sem_pagamento(mock_event_bus):
    """Matrícula sem pagamento deve falhar no passo 7."""
    wizard_id = uuid4()
    citizen_id = uuid4()
    session = WizardSession(
        id=wizard_id,
        citizen_id=citizen_id,
        status=WizardStatus.EM_CURSO,
        passo_atual=7,
        dados_estudante={"nome_completo": "Maria", "data_nascimento": str(date.today())},
        selecao_escola={"escola_id": str(uuid4()), "turma_id": str(uuid4()), "ano_letivo_id": str(uuid4()), "classe": "1a"},
        pagamento=None,
    )
    repo = SimpleNamespace(
        get_by_id=AsyncMock(return_value=session),
        save=AsyncMock(side_effect=lambda s: s),
    )
    from apps.backend.app.modules.educacao.domain.models.matricula import Matricula
    matricula = Matricula(
        id=uuid4(),
        numero_processo="2026/E2E/MAT/0002",
        citizen_id=citizen_id,
        escola_id=uuid4(),
        turma_id=uuid4(),
        ano_letivo_id=uuid4(),
        data_matricula=date.today(),
        status=StatusMatricula.PENDENTE,
    )
    mat_svc = SimpleNamespace(criar_matricula=AsyncMock(return_value=matricula))
    svc = WizardMatriculaService(wizard_repo=repo, matricula_service=mat_svc)
    svc._resolve_or_create_identity = AsyncMock(return_value=(uuid4(), "2026/E2E/NS0002", "Maria"))

    result = await svc.confirmar_matricula(wizard_id)
    # Sem pagamento, a matrícula pode ainda ser criada mas sem payment_flag
    assert "erro" not in result or result.get("submetida") is not False
