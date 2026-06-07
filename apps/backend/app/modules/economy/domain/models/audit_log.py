from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class FinancialAudit:
    """Registro de auditoria financeira simplificado."""

    id: str
    entity_type: str
    entity_id: str
    action: str
    previous_state: dict[str, Any]
    new_state: dict[str, Any]
    timestamp: datetime
    metadata: dict[str, Any] | None = None
