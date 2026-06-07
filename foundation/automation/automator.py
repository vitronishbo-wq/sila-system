from typing import Any

from domain.transfer_automation import execute_transfer
from domain.vacancy_marketplace import VacancyMarketplace
from foundation.automation.message_bus import build_automation_bus
from foundation.eligibility.audit import audit_event
from foundation.eligibility.evaluator import Evaluator
from foundation.orchestration.orchestrator import Orchestrator

_vacancy_marketplace = VacancyMarketplace()


class AutomationEngine:
    def __init__(
        self,
        orchestrator: Orchestrator = None,
        evaluator: Evaluator = None,
        bus=None,
    ):
        self.evaluator = evaluator or Evaluator()
        self.orchestrator = orchestrator
        self.bus = bus if bus is not None else (None if orchestrator is not None else build_automation_bus())

        if self.bus is not None:
            self.bus.subscribe("transfer_requested", self._on_transfer_requested)
            self.bus.subscribe("transfer_validated", self._on_transfer_validated)
            self.bus.start()
        else:
            self.orchestrator = self.orchestrator or Orchestrator()
            self.orchestrator.start()

    def stop(self):
        try:
            if self.orchestrator:
                self.orchestrator.stop()
        except Exception:
            pass
        try:
            if self.bus:
                self.bus.stop()
        except Exception:
            pass

    def request_transfer(self, request: dict[str, Any], async_execute: bool = True) -> dict[str, Any]:
        """Evaluate and schedule/execute a transfer.

        If `async_execute` is True, eligible transfers will be routed through the
        automation message bus or legacy orchestrator.
        """
        if not request.get("institution_capacity") and not request.get("vacancies"):
            try:
                available = _vacancy_marketplace.get_available_for(
                    request.get("target_school"), request.get("target_class")
                )
                request["institution_capacity"] = {"available": available}
            except Exception:
                pass

        eval_out = self.evaluator.evaluate(request)
        payload = {"event_type": "transfer_requested", "request": request, "evaluation": eval_out}
        audit_event("transfer_requested", payload)

        if not eval_out.get("eligible"):
            return {"status": "rejected", "evaluation": eval_out}

        if async_execute and self.bus is not None:
            self.bus.publish("transfer_requested", payload)
            return {"status": "scheduled", "evaluation": eval_out}

        if async_execute:
            self.orchestrator.submit(self._execute_task, request, max_retries=3)
            return {"status": "scheduled", "evaluation": eval_out}

        res = self._execute_task(request)
        return {"status": "executed", "evaluation": eval_out, "result": res}

    def _on_transfer_requested(self, payload: dict[str, Any]) -> None:
        audit_event("transfer_validated", payload)
        self.bus.publish("transfer_validated", payload)

    def _on_transfer_validated(self, payload: dict[str, Any]) -> None:
        request = payload.get("request", {})
        try:
            self._execute_task(request)
        except Exception:
            # _execute_task already emits transfer_failed on error.
            pass

    def _execute_task(self, request: dict[str, Any]):
        try:
            tr = execute_transfer(
                type("TR", (), {
                    "student_id": request.get("student_id"),
                    "target_school_id": request.get("target_school"),
                    "target_class": request.get("target_class"),
                    "academic_year": request.get("academic_year"),
                    "metadata": request.get("metadata", {}),
                })(),
                force=True,
            )
            payload = {
                "event_type": "transfer_completed",
                "student_id": request.get("student_id"),
                "result": {"eligible": tr.eligible, "score": tr.score},
            }
            audit_event("transfer_completed", payload)
            if self.bus is not None:
                self.bus.publish("transfer_completed", payload)
            return tr
        except Exception as e:
            payload = {"event_type": "transfer_failed", "student_id": request.get("student_id"), "error": str(e)}
            audit_event("transfer_failed", payload)
            if self.bus is not None:
                self.bus.publish("transfer_failed", payload)
            raise
