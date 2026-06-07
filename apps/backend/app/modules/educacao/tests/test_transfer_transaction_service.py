from __future__ import annotations

import asyncio
from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock
from uuid import UUID, uuid4

from apps.backend.app.modules.educacao.application.transfer_transaction_service import (
    TransferTransactionService,
)


class FakeAsyncSession:
    class FakeTransaction:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

    def begin(self):
        return FakeAsyncSession.FakeTransaction()


def test_execute_transfer_generates_receipt_and_notifies_student() -> None:
    student_id = uuid4()
    current_enrollment_id = uuid4()
    target_institution_id = uuid4()
    actor_id = uuid4()

    current_enrollment = {
        "id": current_enrollment_id,
        "student_id": student_id,
        "institution_id": uuid4(),
        "status": "ACTIVE",
    }
    academic_identity = {
        "id": student_id,
        "institution_id": current_enrollment["institution_id"],
        "current_grade": "9A",
        "current_shift": "MORNING",
        "birth_date": date(2010, 1, 2),
    }

    citizen_repo = SimpleNamespace(
        get_by_id=AsyncMock(
            return_value=SimpleNamespace(
                full_name="Maria Silva",
                birth_date=date(2010, 1, 2),
                address="Rua das Flores, Luanda",
                province="Luanda",
                vital_status="active",
                is_active=True,
                guardian_name="João Silva",
            )
        )
    )
    candidate_repo = SimpleNamespace(get_by_citizen=AsyncMock(return_value=SimpleNamespace(status=SimpleNamespace(value="ATIVO"))))
    bolsa_repo = SimpleNamespace(list_by_jovem=AsyncMock(return_value=[]))
    propina_repo = SimpleNamespace(exists_active_for_citizen=AsyncMock(return_value=False))

    turma_repo = SimpleNamespace(
        get_by_id=AsyncMock(return_value=SimpleNamespace(capacidade=5)),
        count_matriculas_ativas=AsyncMock(return_value=1),
    )
    capacity_repo = SimpleNamespace(
        reserve_capacity=AsyncMock(
            return_value={"id": uuid4(), "capacity_reserved": 1}
        )
    )
    enrollment_repo = SimpleNamespace(
        get_by_id=AsyncMock(return_value=current_enrollment),
        save=AsyncMock(side_effect=lambda payload: payload),
    )
    academic_identity_repo = SimpleNamespace(
        get_by_id=AsyncMock(return_value=academic_identity),
        save=AsyncMock(side_effect=lambda payload: payload),
    )
    outbox_repo = SimpleNamespace(save=AsyncMock(return_value=SimpleNamespace()))
    audit_service = Mock()
    notification_service = Mock()
    request_service = SimpleNamespace(
        create_education_request=AsyncMock(return_value=uuid4()),
        mark_education_request_completed=AsyncMock(return_value=True),
    )

    service = TransferTransactionService(
        session=FakeAsyncSession(),
        turma_repo=turma_repo,
        capacity_repo=capacity_repo,
        enrollment_repo=enrollment_repo,
        academic_identity_repo=academic_identity_repo,
        citizen_repo=citizen_repo,
        candidate_repo=candidate_repo,
        bolsa_repo=bolsa_repo,
        propina_repo=propina_repo,
        request_service=request_service,
        outbox_repo=outbox_repo,
        audit_service=audit_service,
        notification_service=notification_service,
    )

    result = asyncio.run(
        service.execute_transfer(
            student_id=student_id,
            current_enrollment_id=current_enrollment_id,
            target_institution_id=target_institution_id,
            target_grade="10A",
            target_shift="MORNING",
            academic_year="2026",
            reason="Student requested instant transfer",
            actor_id=actor_id,
            idempotency_key="dummy-key",
        )
    )

    assert result["status"] == "success"
    assert result["receipt"]["student_id"] == str(student_id)
    assert result["receipt"]["target_grade"] == "10A"
    assert result["receipt"]["academic_year"] == "2026"
    assert result["transfer_id"] == result["receipt"]["transfer_id"]
    assert result["old_enrollment_id"] == str(current_enrollment_id)
    assert result["new_enrollment_id"] != result["old_enrollment_id"]
    assert "audit_event" in result
    assert "domain_event" in result

    assert outbox_repo.save.call_count == 4
    audit_service.log.assert_called_once()
    notification_service.send.assert_called_once()
    citizen_repo.get_by_id.assert_awaited_once_with(student_id)
    candidate_repo.get_by_citizen.assert_awaited_once_with(student_id)
    bolsa_repo.list_by_jovem.assert_awaited_once_with(student_id)
    propina_repo.exists_active_for_citizen.assert_awaited_once_with(student_id, "propina")

    called_args, called_kwargs = notification_service.send.call_args
    assert called_kwargs["channel"] == "email"
    assert called_kwargs["to"] == f"student:{student_id}"
    assert "Comprovativo" in called_kwargs["body"]
    assert result["receipt"]["national_validation"]["civil_registry"] is True
    assert result["receipt"]["national_validation"]["financial_clear"] is True

    request_service.create_education_request.assert_awaited_once_with(
        entity_id=current_enrollment_id,
        citizen_id=student_id,
        numero_processo=str(current_enrollment_id),
        escola_nome=f"Transferência para {target_institution_id}",
        ano_letivo="2026",
    )
    request_service.mark_education_request_completed.assert_awaited_once_with(
        entity_id=current_enrollment_id,
        actor_id=actor_id,
        metadata={"transfer_id": result["transfer_id"]},
    )

    audit_called_args, audit_called_kwargs = audit_service.log.call_args
    assert audit_called_kwargs["entity_type"] == "transfer_transaction"
    assert audit_called_kwargs["action"] == "transfer_completed"
    assert audit_called_kwargs["actor"] == str(actor_id)
    assert audit_called_kwargs["after"]["audit_event"]["event_type"] == "TRANSFER_COMPLETED"

def test_execute_transfer_fails_when_citizen_not_in_civil_registry() -> None:
    student_id = uuid4()
    current_enrollment_id = uuid4()
    target_institution_id = uuid4()
    actor_id = uuid4()

    current_enrollment = {
        "id": current_enrollment_id,
        "student_id": student_id,
        "institution_id": uuid4(),
        "status": "ACTIVE",
    }
    academic_identity = {
        "id": student_id,
        "institution_id": current_enrollment["institution_id"],
        "current_grade": "9A",
        "current_shift": "MORNING",
        "birth_date": date(2010, 1, 2),
    }

    turma_repo = SimpleNamespace(
        get_by_id=AsyncMock(return_value=SimpleNamespace(capacidade=5)),
        count_matriculas_ativas=AsyncMock(return_value=1),
    )
    capacity_repo = SimpleNamespace(
        reserve_capacity=AsyncMock(return_value={"id": uuid4(), "capacity_reserved": 1})
    )
    enrollment_repo = SimpleNamespace(
        get_by_id=AsyncMock(return_value=current_enrollment),
        save=AsyncMock(side_effect=lambda payload: payload),
    )
    academic_identity_repo = SimpleNamespace(
        get_by_id=AsyncMock(return_value=academic_identity),
        save=AsyncMock(side_effect=lambda payload: payload),
    )
    citizen_repo = SimpleNamespace(get_by_id=AsyncMock(return_value=None))
    candidate_repo = SimpleNamespace(get_by_citizen=AsyncMock(return_value=None))
    bolsa_repo = SimpleNamespace(list_by_jovem=AsyncMock(return_value=[]))
    propina_repo = SimpleNamespace(exists_active_for_citizen=AsyncMock(return_value=False))

    request_service = SimpleNamespace(
        create_education_request=AsyncMock(return_value=uuid4()),
        mark_education_request_completed=AsyncMock(return_value=True),
    )
    service = TransferTransactionService(
        session=FakeAsyncSession(),
        turma_repo=turma_repo,
        capacity_repo=capacity_repo,
        enrollment_repo=enrollment_repo,
        academic_identity_repo=academic_identity_repo,
        citizen_repo=citizen_repo,
        candidate_repo=candidate_repo,
        bolsa_repo=bolsa_repo,
        propina_repo=propina_repo,
        request_service=request_service,
        outbox_repo=SimpleNamespace(save=AsyncMock(return_value=SimpleNamespace())),
        audit_service=Mock(),
        notification_service=Mock(),
    )

    try:
        asyncio.run(
            service.execute_transfer(
                student_id=student_id,
                current_enrollment_id=current_enrollment_id,
                target_institution_id=target_institution_id,
                target_grade="10A",
                target_shift="MORNING",
                academic_year="2026",
                reason="Student requested instant transfer",
                actor_id=actor_id,
                idempotency_key="dummy-key",
            )
        )
        assert False, "Expected ValueError for missing civil registry citizen"
    except ValueError as exc:
        assert "Identidade Civil" in str(exc)
