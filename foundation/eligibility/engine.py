from typing import Any

from domain.transfer_automation import execute_transfer
from domain.transfer_policy import TransferRequest, TransferResult
from domain.vacancy_marketplace import VacancyMarketplace

from .evaluator import Evaluator

_vacancy_marketplace = VacancyMarketplace()


class EligibilityEngine:
    def __init__(self, evaluator: Evaluator):
        self.evaluator = evaluator

    def evaluate_transfer(self, request: dict[str, Any]) -> TransferResult:
        """Evaluate transfer eligibility and return a TransferResult.

        If the evaluator indicates automatic_execution and the request is eligible,
        the engine will call the transfer automation to execute the transfer.
        """
        # If caller didn't provide capacity info, query the VacancyMarketplace
        if not request.get("institution_capacity") and not request.get("vacancies"):
            try:
                available = _vacancy_marketplace.get_available_for(request.get("target_school"), request.get("target_class"))
                request["institution_capacity"] = {"available": available}
            except Exception:
                # If integration fails, continue and let rules handle missing data
                pass

        eval_out = self.evaluator.evaluate(request)

        tr = TransferResult(
            eligible=bool(eval_out.get("eligible", False)),
            score=int(eval_out.get("score", 0)),
            reasons=eval_out.get("reasons", []),
            automatic_execution=False,
        )

        # If eligible and evaluator recommends automatic execution, call automation
        if tr.eligible and bool(eval_out.get("automatic_execution", False)):
            transfer_request = TransferRequest(
                student_id=request.get("student_id"),
                target_school_id=request.get("target_school"),
                target_class=request.get("target_class"),
                academic_year=request.get("academic_year"),
                metadata=request.get("metadata", {}),
            )
            executed = execute_transfer(transfer_request, force=True)
            return executed

        return tr
