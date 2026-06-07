from foundation.persistence import EducacaoRepository, InfrastructureUnavailableError

from .transfer_policy import TransferResult


def execute_transfer(transfer_request, force: bool = False) -> TransferResult:
    """Execute an eligible transfer and persist the transaction when available."""
    from foundation.eligibility.audit import audit_event

    repository = EducacaoRepository()
    result = TransferResult(eligible=True, score=100, reasons=[], automatic_execution=force)

    try:
        repository.execute_transfer_sync(transfer_request, force=force)
        payload = {
            "request": {
                "student_id": transfer_request.student_id,
                "target_school_id": transfer_request.target_school_id,
                "target_class": transfer_request.target_class,
                "academic_year": transfer_request.academic_year,
            },
            "result": {
                "eligible": result.eligible,
                "score": result.score,
                "automatic_execution": result.automatic_execution,
            },
        }
        audit_event("transfer_executed", payload)
    except InfrastructureUnavailableError as exc:
        audit_event("transfer_failed", {"error": str(exc), "request": transfer_request.__dict__})
        raise
    except Exception as exc:
        audit_event("transfer_failed", {"error": str(exc), "request": transfer_request.__dict__})
        raise

    return result
