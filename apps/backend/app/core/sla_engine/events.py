from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("sla_engine.events")


def emit_event(event_name: str, payload: dict[str, Any]) -> None:
    logger.info("sla_event", extra={"event": event_name, "payload": payload})


def emit_sla_calculated(payload: dict[str, Any]) -> None:
    emit_event("sla.calculated", payload)


def emit_sla_violation(payload: dict[str, Any]) -> None:
    emit_event("sla.violation", payload)


class SLAEventEmitter:
    def policy_created(self, payload: dict[str, Any]) -> None:
        emit_event("sla.policy_created", payload)

    def override_created(self, payload: dict[str, Any]) -> None:
        emit_event("sla.override_created", payload)

    def violation_escalated(self, violation_id: str, level: int) -> None:
        emit_event("sla.violation_escalated", {"violation_id": violation_id, "level": level})
