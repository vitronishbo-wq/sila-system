from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


@dataclass
class CaseCreated:
    event_type: str = "case_created"
    version: int = 1
    case_id: UUID | None = None
    citizen_id: UUID | None = None
    case_type: str = ""
    tribunal: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class CaseClosed:
    event_type: str = "case_closed"
    version: int = 1
    case_id: UUID | None = None
    citizen_id: UUID | None = None
    outcome: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class CertificateRequested:
    event_type: str = "certificate_requested"
    version: int = 1
    certificate_id: UUID | None = None
    citizen_id: UUID | None = None
    certificate_type: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class NotarialActSigned:
    event_type: str = "notarial_act_signed"
    version: int = 1
    act_id: UUID | None = None
    citizen_id: UUID | None = None
    act_type: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


EVENT_CATALOG = {
    "case_created": CaseCreated,
    "case_closed": CaseClosed,
    "certificate_requested": CertificateRequested,
    "notarial_act_signed": NotarialActSigned,
}
