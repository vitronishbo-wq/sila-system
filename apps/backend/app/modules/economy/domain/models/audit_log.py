from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class FinancialAudit:
    """Registro de auditoria financeira simplificado."""
    id: str
    entity_type: str
    entity_id: str
    action: str
    previous_state: Dict[str, Any]
    new_state: Dict[str, Any]
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None
