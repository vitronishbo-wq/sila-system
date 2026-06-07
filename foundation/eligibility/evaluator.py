from typing import Any

from .rules import (
    CompatibleAgeRule,
    HasAvailableVacancyRule,
    NoPendingDebtRule,
    TransferWindowRule,
    ValidAcademicStatusRule,
    WithinTransferDistanceRule,
)
from .scoring import compute_score


class Evaluator:
    def __init__(self, rules: list = None):
        self.rules = rules or [
            HasAvailableVacancyRule(),
            WithinTransferDistanceRule(),
            NoPendingDebtRule(),
            ValidAcademicStatusRule(),
            CompatibleAgeRule(),
            TransferWindowRule(),
        ]

    def evaluate(self, request: dict[str, Any]) -> dict[str, Any]:
        reasons = []
        passed = True
        for rule in self.rules:
            ok, reason = rule.evaluate(request)
            if not ok:
                passed = False
                reasons.append(reason)

        score = compute_score(request, reasons)
        return {
            "eligible": passed,
            "score": score,
            "reasons": reasons,
            "automatic_execution": passed,
        }
