"""
Justice Module Domain Events
ACAO Compliance: All events track official status changes and audit trail.
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, Optional
from uuid import UUID

from apps.backend.app.core.events.domain_event import (
    AuditableEvent,
    ComplianceEvent,
    DomainEvent,
    StatusChangeEvent,
)


@dataclass
class CitizenCreated(AuditableEvent):
    """Emitted when a new citizen is registered."""

    first_name: str = ""
    last_name: str = ""
    birth_date: date | None = None
    birth_place: str = ""
    nationality: str = ""

    def __post_init__(self):
        object.__setattr__(self, "aggregate_type", "Citizen")
        object.__setattr__(self, "event_type", "CitizenCreated")
        super().__post_init__()


@dataclass
class CitizenIdentityDocumentIssued(ComplianceEvent):
    """Emitted when identity document is issued (ACAO compliance)."""

    document_number: str = ""
    document_type: str = ""
    issue_date: date | None = None
    expiry_date: date | None = None
    issuing_authority: str = ""

    def __post_init__(self):
        object.__setattr__(self, "aggregate_type", "Citizen")
        object.__setattr__(self, "event_type", "CitizenIdentityDocumentIssued")
        if not hasattr(self, "metadata") or self.metadata is None:
            object.__setattr__(self, "metadata", {})
        if "compliance_requirement" not in self.metadata:
            self.metadata["compliance_requirement"] = "ACAO_6.2"
        super().__post_init__()


@dataclass
class CitizenStatusChanged(StatusChangeEvent):
    """Track citizen status transitions (active, inactive, archived)."""

    new_status: str = ""
    old_status: str | None = None

    def __post_init__(self):
        object.__setattr__(self, "aggregate_type", "Citizen")
        object.__setattr__(self, "event_type", "CitizenStatusChanged")
        super().__post_init__()


@dataclass
class BirthRecordCreated(AuditableEvent):
    """Birth record registration event."""

    child_name: str = ""
    birth_place: str = ""
    registering_authority: str = ""
    father_id: UUID | None = None
    mother_id: UUID | None = None
    birth_date: date | None = None

    def __post_init__(self):
        object.__setattr__(self, "aggregate_type", "BirthRecord")
        object.__setattr__(self, "event_type", "BirthRecordCreated")
        super().__post_init__()


@dataclass
class BirthRecordCertificateIssued(ComplianceEvent):
    """Birth certificate issuance (ACAO requirement)."""

    certificate_number: str = ""
    issued_date: date | None = None
    serial_number: str = ""

    def __post_init__(self):
        object.__setattr__(self, "aggregate_type", "BirthRecord")
        object.__setattr__(self, "event_type", "BirthRecordCertificateIssued")
        super().__post_init__()


@dataclass
class MarriageRecorded(AuditableEvent):
    """Marriage registration event."""

    first_spouse_id: UUID | None = None
    second_spouse_id: UUID | None = None
    celebration_date: date | None = None
    registration_date: date | None = None
    registering_authority: str = ""

    def __post_init__(self):
        object.__setattr__(self, "aggregate_type", "MarriageRecord")
        object.__setattr__(self, "event_type", "MarriageRecorded")
        super().__post_init__()


@dataclass
class MarriageCertificateIssued(ComplianceEvent):
    """Marriage certificate issuance."""

    certificate_number: str = ""
    issued_date: date | None = None

    def __post_init__(self):
        object.__setattr__(self, "aggregate_type", "MarriageRecord")
        object.__setattr__(self, "event_type", "MarriageCertificateIssued")
        super().__post_init__()


@dataclass
class DeathRecorded(AuditableEvent):
    """Death registration event."""

    deceased_id: UUID | None = None
    death_date: date | None = None
    death_place: str = ""
    registering_authority: str = ""
    cause_of_death: str | None = None

    def __post_init__(self):
        object.__setattr__(self, "aggregate_type", "DeathRecord")
        object.__setattr__(self, "event_type", "DeathRecorded")
        super().__post_init__()


@dataclass
class DeathCertificateIssued(ComplianceEvent):
    """Death certificate issuance."""

    certificate_number: str = ""
    issued_date: date | None = None

    def __post_init__(self):
        object.__setattr__(self, "aggregate_type", "DeathRecord")
        object.__setattr__(self, "event_type", "DeathCertificateIssued")
        super().__post_init__()


__all__ = [
    "CitizenCreated",
    "CitizenIdentityDocumentIssued",
    "CitizenStatusChanged",
    "BirthRecordCreated",
    "BirthRecordCertificateIssued",
    "MarriageRecorded",
    "MarriageCertificateIssued",
    "DeathRecorded",
    "DeathCertificateIssued",
]
