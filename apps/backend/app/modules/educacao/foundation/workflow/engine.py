from __future__ import annotations

import datetime
import uuid
from typing import Any


class WorkflowEngine:
    """Lightweight workflow engine with in-memory state persistence.

    For production persist states through `WorkflowPort` and implement
    durable task execution (Celery, Temporal, etc.).
    """

    def __init__(self) -> None:
        self._store: dict[str, dict[str, Any]] = {}

    def start(self, process_type: str, context: dict[str, Any], initiator_id: str) -> str:
        process_id = str(uuid.uuid4())
        state = {
            "id": process_id,
            "type": process_type,
            "context": context,
            "initiator": initiator_id,
            "status": "started",
            "steps": [],
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        }
        self._store[process_id] = state
        return process_id

    def approve_step(self, process_id: str, step: str, user_id: str, payload: dict[str, Any] | None = None) -> None:
        state = self._store.get(process_id)
        if not state:
            raise KeyError("process not found")
        state.setdefault("steps", []).append({"step": step, "actor": user_id, "payload": payload, "ts": datetime.datetime.utcnow().isoformat() + "Z"})
        # simple state transition example
        state["status"] = "in_progress"

    def escalate(self, process_id: str) -> None:
        state = self._store.get(process_id)
        if not state:
            raise KeyError("process not found")
        state["status"] = "escalated"

    def get_state(self, process_id: str) -> dict[str, Any] | None:
        return self._store.get(process_id)
