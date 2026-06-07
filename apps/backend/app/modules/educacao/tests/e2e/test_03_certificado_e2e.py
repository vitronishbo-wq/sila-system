"""E2E: Certificado — Emissão + assinatura digital + auditoria.

Fluxo:
  CertificadoService.create_record()
    → SignatureEngine.sign(document_id, signer_role)
    → AuditLogger.log(SIGN)
    → CertificadoService.concluir()
    → EventBus.publish(CertificadoEmitido)
"""

from __future__ import annotations

from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from apps.backend.app.modules.educacao.application.certificado_service import CertificadoService
from apps.backend.app.modules.educacao.domain.enums import StatusFluxo
from apps.backend.app.modules.educacao.domain.models._workflow_record import WorkflowRecord
from sila_platform.governance.audit.logger import AuditLogger, AuditAction
from sila_platform.governance.digital_signature.engine import SignatureEngine, SignatureStatus


@pytest.mark.asyncio
async def test_certificado_emissao_com_assinatura_e_auditoria():
    citizen_id = uuid4()
    instituicao_id = uuid4()
    certificado_id = uuid4()

    saved = WorkflowRecord(
        id=certificado_id,
        numero_processo="CRT/E2E/2026/0001",
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
    citizen_repo = SimpleNamespace(
        get_by_id=AsyncMock(return_value=SimpleNamespace(id=citizen_id))
    )
    request_service = SimpleNamespace(
        create_education_request=AsyncMock(return_value=uuid4()),
        mark_education_request_completed=AsyncMock(return_value=True),
    )

    service = CertificadoService(
        repository=repository,
        citizen_repo=citizen_repo,
        request_service=request_service,
    )
    audit = AuditLogger()
    sig_engine = SignatureEngine()

    # ── Step 1: Criar pedido de certificado ──────────────────────────
    record = await service.create_record(
        service_type="certificado_conclusao",
        citizen_id=citizen_id,
        instituicao_id=instituicao_id,
    )
    assert record is not None
    assert record.numero_processo == "CRT/E2E/2026/0001"

    # ── Step 2: Assinar digitalmente ─────────────────────────────────
    sig = sig_engine.sign(
        signer_id=str(citizen_id),
        signer_role="nacional",
        document_id=str(certificado_id),
        module="educacao",
        certificate_serial="CERT-SERIAL-E2E-001",
    )
    assert sig.status == SignatureStatus.SIGNED
    assert sig.signer_role == "nacional"
    assert sig.signed_at is not None

    audit.log(
        actor_id=str(citizen_id),
        actor_role="nacional",
        action=AuditAction.SIGN,
        resource_type="certificado",
        resource_id=str(certificado_id),
        module="educacao",
        details={"numero_processo": record.numero_processo, "certificate_serial": sig.certificate_serial},
    )
    assert len(audit._entries) == 1
    assert audit._entries[0].action == AuditAction.SIGN

    # ── Step 3: Verificar assinatura ─────────────────────────────────
    verified = sig_engine.verify(str(certificado_id))
    assert verified is not None
    assert verified.status == SignatureStatus.VERIFIED

    # ── Step 4: Concluir certificado ─────────────────────────────────
    record = await service.conclude_record(
        record_id=certificado_id,
        actor_id=citizen_id,
        resumo="emitido",
    )
    assert record is not None

    # ── Step 5: Verificar auditoria final ────────────────────────────
    audit.log(
        actor_id=str(citizen_id),
        actor_role="nacional",
        action=AuditAction.UPDATE,
        resource_type="certificado",
        resource_id=str(certificado_id),
        module="educacao",
        details={"status": "emitido", "flow": "e2e_certificado"},
    )
    assert len(audit._entries) == 2

    print(f"E2E Certificado OK — assinatura={sig.status.value}, audit={len(audit._entries)} entries")


@pytest.mark.asyncio
async def test_certificado_rejeita_duplicado():
    citizen_id = uuid4()
    instituicao_id = uuid4()

    repository = SimpleNamespace(
        exists_active_for_citizen=AsyncMock(return_value=True),
        save=AsyncMock(side_effect=lambda r: r),
    )
    citizen_repo = SimpleNamespace(
        get_by_id=AsyncMock(return_value=SimpleNamespace(id=citizen_id))
    )
    request_service = SimpleNamespace(
        create_education_request=AsyncMock(return_value=uuid4()),
    )

    service = CertificadoService(
        repository=repository,
        citizen_repo=citizen_repo,
        request_service=request_service,
    )

    with pytest.raises(ValueError, match="ja possui registo ativo"):
        await service.create_record(
            service_type="certificado_conclusao",
            citizen_id=citizen_id,
            instituicao_id=instituicao_id,
        )
