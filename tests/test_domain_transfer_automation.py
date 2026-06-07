from unittest.mock import Mock, patch

from domain.transfer_automation import execute_transfer
from domain.transfer_policy import TransferRequest
from foundation.persistence import InfrastructureUnavailableError


def test_execute_transfer_uses_foundation_repository_and_audits_execution():
    repository = Mock()
    repository.execute_transfer_sync.return_value = None

    with patch("domain.transfer_automation.EducacaoRepository", return_value=repository), patch(
        "foundation.eligibility.audit.audit_event",
    ) as audit_event:
        request = TransferRequest(
            student_id="student-1",
            target_school_id="school-dest",
            target_class="7B",
            academic_year="2026",
            metadata={"reason": "relocation"},
        )
        result = execute_transfer(request, force=True)

    repository.execute_transfer_sync.assert_called_once_with(request, force=True)
    assert result.eligible is True
    assert result.automatic_execution is True
    audit_event.assert_any_call("transfer_executed", {
        "request": {
            "student_id": "student-1",
            "target_school_id": "school-dest",
            "target_class": "7B",
            "academic_year": "2026",
        },
        "result": {
            "eligible": True,
            "score": 100,
            "automatic_execution": True,
        },
    })


def test_execute_transfer_fails_when_infrastructure_unavailable():
    repository = Mock()
    repository.execute_transfer_sync.side_effect = InfrastructureUnavailableError("db down")

    with patch("domain.transfer_automation.EducacaoRepository", return_value=repository), patch(
        "foundation.eligibility.audit.audit_event",
    ) as audit_event:
        request = TransferRequest(
            student_id="student-2",
            target_school_id="school-dest",
            target_class="7B",
            academic_year="2026",
            metadata={},
        )
        try:
            execute_transfer(request, force=False)
            assert False, "Expected InfrastructureUnavailableError"
        except InfrastructureUnavailableError:
            pass

    repository.execute_transfer_sync.assert_called_once_with(request, force=False)
    audit_event.assert_any_call("transfer_failed", {"error": "db down", "request": request.__dict__})
