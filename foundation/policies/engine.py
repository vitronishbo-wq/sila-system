from __future__ import annotations

import datetime
import json
import os
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class PolicyDefinition:
    name: str
    value: Any
    description: str = ""
    evaluator: Callable[[Any, dict[str, Any]], Any] | None = None


class PolicyEngine:
    """Central registry for policy values and rule evaluation.

    Features added:
    - optional JSON persistence (path from `POLICY_STORE_PATH` env var)
    - simple append-only audit of updates in `data/policies_audit.log`
    - `register_policy` is non-destructive by default (won't overwrite persisted values)
    """

    def __init__(self) -> None:
        self._policies: dict[str, PolicyDefinition] = {}
        self._store_path = os.getenv("POLICY_STORE_PATH", "data/policies.json")
        self._audit_path = os.getenv("POLICY_AUDIT_PATH", "data/policies_audit.log")
        # Try to load persisted overrides (non-fatal)
        try:
            self._load_store()
        except Exception:
            # If loading fails, start with empty in-memory store; defaults will register after import
            pass

    def _audit(self, action: str, name: str | None = None, before: Any | None = None, after: Any | None = None) -> None:
        record = {
            "ts": datetime.datetime.utcnow().isoformat() + "Z",
            "action": action,
            "policy": name,
            "before": before,
            "after": after,
        }
        try:
            os.makedirs(os.path.dirname(self._audit_path), exist_ok=True)
            with open(self._audit_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, default=str) + "\n")
        except Exception:
            # Best-effort auditing
            pass

    def _load_store(self) -> None:
        if not os.path.exists(self._store_path):
            return
        try:
            with open(self._store_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            if isinstance(raw, dict):
                for k, v in raw.items():
                    # preserve existing in-memory definitions (defaults) unless explicitly overridden
                    self._policies[k] = PolicyDefinition(name=k, value=v.get("value", v), description=v.get("description", ""))
        except Exception:
            # ignore load errors — engine stays in-memory
            pass

    def _save_store(self) -> None:
        try:
            os.makedirs(os.path.dirname(self._store_path), exist_ok=True)
            payload = {name: {"value": p.value, "description": p.description} for name, p in self._policies.items()}
            with open(self._store_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, default=str, indent=2)
        except Exception:
            # Best-effort persistence
            pass

    def register_policy(self, name: str, value: Any, description: str = "", overwrite: bool = False) -> None:
        """Register a policy definition.

        By default `register_policy` is non-destructive: it won't overwrite an existing
        policy that may have been loaded from persistent store. Pass `overwrite=True`
        to replace an existing value.
        """
        if name in self._policies and not overwrite:
            return
        self._policies[name] = PolicyDefinition(name=name, value=value, description=description)

    def get_policy(self, name: str, default: Any = None) -> Any:
        return self._policies.get(name, PolicyDefinition(name=name, value=default)).value

    def update_policy(self, name: str, value: Any) -> None:
        before = self._policies.get(name).value if name in self._policies else None
        if name in self._policies:
            self._policies[name].value = value
        else:
            self.register_policy(name, value)
        # persist and audit (best-effort)
        self._save_store()
        self._audit("policy_update", name=name, before=before, after=value)

    def register_batch(self, policies: dict[str, Any]) -> None:
        for name, payload in policies.items():
            if isinstance(payload, dict) and "value" in payload:
                self.register_policy(name, payload["value"], description=payload.get("description", ""))
            else:
                self.register_policy(name, payload)

    def list_policies(self) -> dict[str, Any]:
        return {name: policy.value for name, policy in self._policies.items()}


policy_engine = PolicyEngine()
