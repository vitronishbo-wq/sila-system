"""
Documents Module Domain Events
ACAO Compliance: All events track document management and issuance.
"""

from datetime import date
from typing import Optional
from uuid import UUID

from apps.backend.app.core.events.domain_event import (
    AuditableEvent,
    ComplianceEvent,
    DomainEvent,
    StatusChangeEvent,
)


class DocumentRegistered(AuditableEvent):
    """Emitted when a document is registered."""

    document_id: UUID
    document_type: str
    title: str
    registration_date: date
    created_by: str = ""
    subject_id: UUID = None

    def __post_init__(self):
        self.aggregate_type = "Document"
        self.event_type = "DocumentRegistered"
        super().__post_init__()


class DocumentStatusChanged(StatusChangeEvent):
    """Track document status transitions (draft, approved, archived, destroyed)."""

    document_id: UUID
    reason: str = ""

    def __post_init__(self):
        self.aggregate_type = "Document"
        self.event_type = "DocumentStatusChanged"
        super().__post_init__()


class OfficialDocumentIssued(ComplianceEvent):
    """Emitted when official document is issued (ACAO compliance)."""

    document_id: UUID
    document_number: str
    issue_date: date
    expiry_date: date | None = None
    issuing_authority: str = ""
    recipient_id: UUID = None

    def __post_init__(self):
        self.aggregate_type = "OfficialDocument"
        self.event_type = "OfficialDocumentIssued"
        super().__post_init__()


class DocumentAuthenticated(ComplianceEvent):
    """Emitted when document authenticity is verified."""

    document_id: UUID
    authentication_date: date
    authenticated_by: str = ""
    authentication_method: str = ""

    def __post_init__(self):
        self.aggregate_type = "Document"
        self.event_type = "DocumentAuthenticated"
        super().__post_init__()


class DocumentArchived(ComplianceEvent):
    """Emitted when document is archived per retention policy."""

    document_id: UUID
    archive_date: date
    retention_period: str = ""
    archive_location: str = ""
    archived_by: str = ""

    def __post_init__(self):
        self.aggregate_type = "Document"
        self.event_type = "DocumentArchived"
        super().__post_init__()
