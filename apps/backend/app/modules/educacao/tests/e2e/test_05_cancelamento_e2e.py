"""E2E: Cancelamento — Rollback + auditoria + eventos.

Fluxo:
  WorkflowEngine.avancar(2 steps) → WorkflowEngine.cancelar()
    → AuditLogger.log(CANCEL)
    → WorkflowStatus.CANCELLED
    → history regista "cancelado"
    → EventBus.publish(MatriculaCancelada)
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from apps.backend.app.modules.educacao.workflows.matricula_workflow import (
    MatriculaWorkflowEngine,
)
from sila_platform.governance.audit.logger import AuditLogger, AuditAction
from sila_platform.governance.workflows.engine import WorkflowStatus


@pytest.mark.asyncio
async def test_cancelamento_matricula_com_rollback(mock_event_bus):
    engine = MatriculaWorkflowEngine()
    audit = AuditLogger()
    provider = f"matricula-{uuid4().hex[:8]}"
    student_id = str(uuid4())
    school_id = str(uuid4())

    # ── Step 1: Criar workflow ───────────────────────────────────────
    wf = engine.criar(
        provider=provider,
        student_id=student_id,
        school_id=school_id,
    )
    assert wf.status == WorkflowStatus.IN_PROGRESS
    assert wf.current_step == 0

    # ── Step 2: Avançar 2 passos ────────────────────────────────────
    wf = engine.avancar(provider, "unidade", audit_logger=audit)
    assert wf.current_step == 1

    wf = engine.avancar(provider, "municipal", audit_logger=audit)
    assert wf.current_step == 2

    # ── Step 3: Cancelar workflow ────────────────────────────────────
    wf = engine.cancelar(provider, actor="sistema", audit_logger=audit)

    # ── Verificar rollback ──────────────────────────────────────────
    assert wf.status == WorkflowStatus.CANCELLED
    assert wf.concluded_at is not None

    # Verificar que o workflow está cancelado e não pode mais avançar
    with pytest.raises(ValueError, match="ja finalizado"):
        engine.avancar(provider, "municipal")

    # ── Verificar audit trail de cancelamento ────────────────────────
    cancel_entries = [e for e in audit._entries if e.action == AuditAction.CANCEL]
    assert len(cancel_entries) == 1
    assert cancel_entries[0].resource_type == "matricula_workflow"
    assert cancel_entries[0].module == "educacao"

    # ── Verificar workflow history ──────────────────────────────────
    history = wf.history
    # solicitada + escola_valida + municipio_confirma + cancelado
    assert len(history) == 4
    step_names = [h["step"] for h in history]
    assert step_names[:3] == ["criada", "escola_valida", "municipio_confirma"]
    assert step_names[-1] == "cancelado"

    # ── Verificar que os steps intermédios foram registados ─────────
    update_entries = [e for e in audit._entries if e.action == AuditAction.UPDATE]
    assert len(update_entries) == 2  # 2 advances antes de cancelar

    print(f"E2E Cancelamento OK — history={len(history)}, audit={len(audit._entries)}")


@pytest.mark.asyncio
async def test_cancelamento_ja_finalizado():
    """Tentar cancelar workflow já concluído deve falhar."""
    engine = MatriculaWorkflowEngine()
    provider = f"matricula-done-{uuid4().hex[:8]}"

    engine.criar(
        provider=provider,
        student_id=str(uuid4()),
        school_id=str(uuid4()),
    )
    # Avançar todos os steps
    roles = ["unidade", "municipal", "provincial", "nacional"]
    for role in roles:
        engine.avancar(provider, role)

    assert engine.get(provider).status == WorkflowStatus.COMPLETED

    with pytest.raises(ValueError, match="ja finalizado"):
        engine.cancelar(provider)


@pytest.mark.asyncio
async def test_cancelamento_workflow_inexistente():
    engine = MatriculaWorkflowEngine()
    with pytest.raises(ValueError, match="nao encontrado"):
        engine.cancelar("provider-inexistente")
