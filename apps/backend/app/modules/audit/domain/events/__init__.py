"""
Audit Module Domain Events
ACAO Compliance: All events track audits and internal controls.
"""
from uuid import UUID
from datetime import date
from typing import Optional
from apps.backend.app.core.events.domain_event import DomainEvent, AuditableEvent, ComplianceEvent, StatusChangeEvent

class AuditProgramCreated(AuditableEvent):
    """Emitted when an audit program is created."""
    program_id: UUID
    program_name: str
    audit_type: str
    start_date: date
    end_date: date
    auditee_id: UUID = None

    def __post_init__(self):
        self.aggregate_type = 'AuditProgram'
        self.event_type = 'AuditProgramCreated'
        super().__post_init__()

class AuditExecutionStarted(AuditableEvent):
    """Emitted when an audit is started."""
    audit_id: UUID
    program_id: UUID
    execution_date: date
    audit_team: str = ''
    scope: str = ''

    def __post_init__(self):
        self.aggregate_type = 'Audit'
        self.event_type = 'AuditExecutionStarted'
        super().__post_init__()

class AuditFindingReported(ComplianceEvent):
    """Emitted when an audit finding is reported (ACAO compliance)."""
    finding_id: UUID
    audit_id: UUID
    area_of_concern: str
    finding_date: date
    severity: str = 'medium'
    recommended_action: str = ''

    def __post_init__(self):
        self.aggregate_type = 'AuditFinding'
        self.event_type = 'AuditFindingReported'
        super().__post_init__()

class AuditReportSubmitted(ComplianceEvent):
    """Emitted when audit report is submitted."""
    report_id: UUID
    audit_id: UUID
    submission_date: date
    report_summary: str = ''
    submitted_by: str = ''

    def __post_init__(self):
        self.aggregate_type = 'AuditReport'
        self.event_type = 'AuditReportSubmitted'
        super().__post_init__()

class ControllerRecommendationIssued(ComplianceEvent):
    """Emitted when controller issues recommendation from audit."""
    recommendation_id: UUID
    foundation_audit_id: UUID
    recommendation_type: str
    issue_date: date
    deadline_for_action: Optional[date] = None
    issued_by: str = ''

    def __post_init__(self):
        self.aggregate_type = 'ControllerRecommendation'
        self.event_type = 'ControllerRecommendationIssued'
        super().__post_init__()