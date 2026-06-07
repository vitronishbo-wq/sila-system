"""E2E: Transferência — Escola → Município → Província workflow completo.

Fluxo:
  TransferenciaWorkflowEngine.criar()
    → avancar(escola_origem)
    → avancar(escola_destino)
    → avancar(municipio)
    → avancar(provincia)
    → concluido
  Cada passo verificado com AuditLogger e workflow_history.
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from apps.backend.app.modules.educacao.workflows.transferencia_workflow import (
    TransferenciaWorkflowEngine,
)
from sila_platform.governance.audit.logger import AuditLogger, AuditAction
from sila_platform.governance.workflows.engine import WorkflowStatus


@pytest.mark.asyncio
async def test_transferencia_workflow_completo():
    engine = TransferenciaWorkflowEngine()
    audit = AuditLogger()
    provider = f"transfer-{uuid4().hex[:8]}"
    student_id = str(uuid4())
    school_origin = str(uuid4())
    school_dest = str(uuid4())
    mun_id = str(uuid4())
    prov_id = str(uuid4())

    # ── Step 1: Criar pedido de transferência ────────────────────────
    wf = engine.criar(
        provider=provider,
        student_id=student_id,
        school_origin_id=school_origin,
        school_destination_id=school_dest,
        municipality_id=mun_id,
        province_id=prov_id,
    )
    assert wf.status == WorkflowStatus.IN_PROGRESS
    assert wf.current_step == 0
    assert len(wf.history) == 1  # "solicitada" registada no create

    # ── Step 2: Escola origem valida ─────────────────────────────────
    wf = engine.avancar(provider, "unidade", audit_logger=audit)
    assert wf.current_step == 1
    assert len(audit._entries) == 1
    assert audit._entries[0].action == AuditAction.UPDATE

    # ── Step 3: Escola destino aceita ────────────────────────────────
    wf = engine.avancar(provider, "unidade", audit_logger=audit)
    assert wf.current_step == 2

    # ── Step 4: Município confirma ───────────────────────────────────
    wf = engine.avancar(provider, "municipal", audit_logger=audit)
    assert wf.current_step == 3

    # ── Step 5: Província audita ────────────────────────────────────
    wf = engine.avancar(provider, "provincial", audit_logger=audit)
    assert wf.current_step == 4

    # ── Step 6: Concluído ───────────────────────────────────────────
    wf = engine.avancar(provider, "nacional", audit_logger=audit)
    assert wf.status == WorkflowStatus.COMPLETED
    assert wf.current_step == 5
    assert wf.concluded_at is not None

    # ── Verificações finais ─────────────────────────────────────────
    assert len(wf.history) == 6  # 1 create + 5 advances
    assert len(audit._entries) == 5  # 5 advances logged (create não logged aqui)
    for entry in audit._entries:
        assert entry.module == "educacao"

    # Verificar histórico do workflow
    step_names = [h["step"] for h in wf.history]
    assert step_names == [
        "solicitada", "escola_origem_valida", "escola_destino_aceita",
        "municipio_confirma", "provincia_audita", "concluido",
    ]

    print(f"E2E Transferência OK — {len(wf.history)} steps, {len(audit._entries)} audit entries")


@pytest.mark.asyncio
async def test_transferencia_cancelamento():
    engine = TransferenciaWorkflowEngine()
    audit = AuditLogger()
    provider = f"transfer-cancel-{uuid4().hex[:8]}"

    engine.criar(
        provider=provider,
        student_id=str(uuid4()),
        school_origin_id=str(uuid4()),
        school_destination_id=str(uuid4()),
    )
    engine.cancelar(provider, actor="municipal", audit_logger=audit)

    wf = engine.get(provider)
    assert wf.status == WorkflowStatus.CANCELLED
    assert len(audit._entries) == 1
    assert audit._entries[0].action == AuditAction.CANCEL


@pytest.mark.asyncio
async def test_transferencia_rejeita_actor_errado():
    engine = TransferenciaWorkflowEngine()
    provider = f"transfer-reject-{uuid4().hex[:8]}"

    engine.criar(
        provider=provider,
        student_id=str(uuid4()),
        school_origin_id=str(uuid4()),
        school_destination_id=str(uuid4()),
    )
    # Tentar avançar com papel errado (nacional em vez de unidade)
    with pytest.raises(PermissionError):
        engine.avancar(provider, "nacional")
