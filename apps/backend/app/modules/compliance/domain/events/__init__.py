"""
Compliance Module Domain Events
ACAO Compliance: All events track compliance obligations and enforcement.
"""
from uuid import UUID
from datetime import date
from typing import Optional
from apps.backend.app.core.events.domain_event import DomainEvent, AuditableEvent, ComplianceEvent, StatusChangeEvent

class ComplianceObligationCreated(AuditableEvent):
    """Emitted when a compliance obligation is created."""
    obligation_id: UUID
    subject_id: UUID
    obligation_type: str
    description: str = ''
    due_date: date = None

    def __post_init__(self):
        self.aggregate_type = 'ComplianceObligation'
        self.event_type = 'ComplianceObligationCreated'
        super().__post_init__()

class ComplianceObligationStatusChanged(StatusChangeEvent):
    """Track compliance obligation status (pending, compliant, violated)."""
    obligation_id: UUID
    subject_id: UUID
    reason: str = ''

    def __post_init__(self):
        self.aggregate_type = 'ComplianceObligation'
        self.event_type = 'ComplianceObligationStatusChanged'
        super().__post_init__()

class ComplianceInspectionConducted(ComplianceEvent):
    """Emitted when compliance inspection is conducted (ACAO requirement)."""
    inspection_id: UUID
    subject_id: UUID
    inspection_date: date
    inspector_id: str = ''
    findings: str = ''

    def __post_init__(self):
        self.aggregate_type = 'ComplianceInspection'
        self.event_type = 'ComplianceInspectionConducted'
        super().__post_init__()

class ComplianceViolationReported(ComplianceEvent):
    """Emitted when compliance violation is reported."""
    violation_id: UUID
    subject_id: UUID
    violation_type: str
    violation_date: date
    severity_level: str = 'medium'
    reported_by: str = ''

    def __post_init__(self):
        self.aggregate_type = 'ComplianceViolation'
        self.event_type = 'ComplianceViolationReported'
        super().__post_init__()

class ComplianceCertificateIssued(ComplianceEvent):
    """Emitted when compliance certificate is issued."""
    certificate_id: UUID
    subject_id: UUID
    certificate_type: str
    issue_date: date
    expiry_date: Optional[date] = None
    issuing_authority: str = ''

    def __post_init__(self):
        self.aggregate_type = 'ComplianceCertificate'
        self.event_type = 'ComplianceCertificateIssued'
        super().__post_init__()