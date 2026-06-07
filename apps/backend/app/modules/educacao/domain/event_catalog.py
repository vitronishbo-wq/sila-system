from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4


@dataclass
class SeatReserved:
    event_type: str = "seat_reserved"
    version: int = 1
    reservation_id: UUID | None = None
    student_id: UUID | None = None
    institution_id: UUID | None = None
    classe: str = ""
    turno: str = ""
    ano_letivo: str = ""
    expires_at: datetime | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class SeatConfirmed:
    event_type: str = "seat_confirmed"
    version: int = 1
    reservation_id: UUID | None = None
    student_id: UUID | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class SeatExpired:
    event_type: str = "seat_expired"
    version: int = 1
    reservation_id: UUID | None = None
    student_id: UUID | None = None
    vacancy_released: bool = False
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class SeatCancelled:
    event_type: str = "seat_cancelled"
    version: int = 1
    reservation_id: UUID | None = None
    student_id: UUID | None = None
    vacancy_released: bool = False
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class EnrollmentCreated:
    event_type: str = "enrollment_created"
    version: int = 1
    enrollment_id: UUID | None = None
    student_id: UUID | None = None
    institution_id: UUID | None = None
    reservation_id: UUID | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class EnrollmentCompleted:
    event_type: str = "enrollment_completed"
    version: int = 1
    enrollment_id: UUID | None = None
    student_id: UUID | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class TransferStarted:
    event_type: str = "transfer_started"
    version: int = 1
    transfer_id: UUID | None = None
    student_id: UUID | None = None
    origem_escola_id: UUID | None = None
    destino_escola_id: UUID | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class TransferCompleted:
    event_type: str = "transfer_completed"
    version: int = 1
    transfer_id: UUID | None = None
    student_id: UUID | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class TransferFailed:
    event_type: str = "transfer_failed"
    version: int = 1
    transfer_id: UUID | None = None
    student_id: UUID | None = None
    motivo: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None




@dataclass
class IdentityCreated:
    event_type: str = "identity_created"
    version: int = 1
    identity_id: UUID | None = None
    national_student_number: str = ""
    full_name: str = ""
    birth_date: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class IdentityResolved:
    event_type: str = "identity_resolved"
    version: int = 1
    identity_id: UUID | None = None
    match_type: str = ""
    confidence: str = ""
    search_criteria: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class IdentityDuplicateDetected:
    event_type: str = "identity_duplicate_detected"
    version: int = 1
    identity_id: UUID | None = None
    duplicate_of: UUID | None = None
    match_type: str = ""
    confidence: str = ""
    matched_fields: list[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class IdentityMergeRequested:
    event_type: str = "identity_merge_requested"
    version: int = 1
    merge_id: UUID | None = None
    primary_identity_id: UUID | None = None
    duplicate_identity_id: UUID | None = None
    confidence: str = ""
    reason: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class IdentityMerged:
    event_type: str = "identity_merged"
    version: int = 1
    merge_id: UUID | None = None
    primary_identity_id: UUID | None = None
    duplicate_identity_id: UUID | None = None
    merged_fields: list[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


EVENT_CATALOG = {
    "seat_reserved": SeatReserved,
    "seat_confirmed": SeatConfirmed,
    "seat_expired": SeatExpired,
    "seat_cancelled": SeatCancelled,
    "enrollment_created": EnrollmentCreated,
    "enrollment_completed": EnrollmentCompleted,
    "transfer_started": TransferStarted,
    "transfer_completed": TransferCompleted,
    "transfer_failed": TransferFailed,
    "identity_created": IdentityCreated,
    "identity_resolved": IdentityResolved,
    "identity_duplicate_detected": IdentityDuplicateDetected,
    "identity_merge_requested": IdentityMergeRequested,
    "identity_merged": IdentityMerged,
}
