"""
Identity Module Domain Events
ACAO Compliance: All events track identity verification and document issuance.
"""
from uuid import UUID
from datetime import date
from typing import Optional
from apps.backend.app.core.events.domain_event import DomainEvent, AuditableEvent, ComplianceEvent, StatusChangeEvent

class IdentityDocumentRequested(AuditableEvent):
    """Emitted when an identity document is requested."""
    citizen_id: UUID
    document_type: str
    request_reason: str = ''
    issuing_authority: str = ''

    def __post_init__(self):
        self.aggregate_type = 'IdentityDocument'
        self.event_type = 'IdentityDocumentRequested'
        super().__post_init__()

class IdentityDocumentVerified(ComplianceEvent):
    """Emitted when identity is verified and approved (ACAO compliance)."""
    citizen_id: UUID
    verification_level: str
    verified_by: str = ''
    verification_date: date = None

    def __post_init__(self):
        self.aggregate_type = 'IdentityDocument'
        self.event_type = 'IdentityDocumentVerified'
        super().__post_init__()

class IdentityDocumentStatusChanged(StatusChangeEvent):
    """Track identity document status transitions."""
    citizen_id: UUID
    document_type: str

    def __post_init__(self):
        self.aggregate_type = 'IdentityDocument'
        self.event_type = 'IdentityDocumentStatusChanged'
        super().__post_init__()

class BiometricDataEnrolled(ComplianceEvent):
    """Emitted when biometric data is enrolled for identity."""
    citizen_id: UUID
    biometric_type: str
    enrollment_date: date = None
    enrolled_by: str = ''

    def __post_init__(self):
        self.aggregate_type = 'BiometricData'
        self.event_type = 'BiometricDataEnrolled'
        super().__post_init__()

class IdentityCredentialIssued(ComplianceEvent):
    """Emitted when identity credential is issued."""
    credential_number: str
    credential_type: str
    issue_date: date
    expiry_date: Optional[date] = None
    issuing_authority: str = ''

    def __post_init__(self):
        self.aggregate_type = 'IdentityCredential'
        self.event_type = 'IdentityCredentialIssued'
        super().__post_init__()