"""Tipos de eventos de domínio usados pelos bounded contexts."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

@dataclass(slots=True)
class DomainEvent:
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass(slots=True)
class CitizenValidated(DomainEvent):
    citizen_id: str = ''
    status: str = 'ACTIVE'
    full_name: str = ''
    document_type: str = ''

@dataclass(slots=True)
class CitizenValidationFailed(DomainEvent):
    citizen_id: str = ''
    reason: str = 'UNKNOWN'
    details: dict[str, Any] = field(default_factory=dict)
