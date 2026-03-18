from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict
from uuid import uuid4

@dataclass(slots=True)
class BaseEvent:
    """Lightweight base event compatible with outbox persistence."""
    aggregate_id: str
    payload: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_type: str = 'GENERIC_EVENT'