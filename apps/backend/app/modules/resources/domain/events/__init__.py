"""
Resources Module Domain Events
ACAO Compliance: All events track natural resources and exploitation rights.
"""
from uuid import UUID
from datetime import date
from typing import Optional
from apps.backend.app.core.events.domain_event import DomainEvent, AuditableEvent, ComplianceEvent, StatusChangeEvent

class ResourceExplorationLicenseApplied(AuditableEvent):
    """Emitted when exploration license is applied."""
    application_id: UUID
    applicant_id: UUID
    resource_type: str
    location: str = ''
    application_date: date = None

    def __post_init__(self):
        self.aggregate_type = 'ResourceExploration'
        self.event_type = 'ResourceExplorationLicenseApplied'
        super().__post_init__()

class ExploitationLicenseIssued(ComplianceEvent):
    """Emitted when exploitation license is issued (ACAO compliance)."""
    license_id: UUID
    applicant_id: UUID
    license_number: str
    resource_type: str
    issue_date: date
    expiry_date: Optional[date] = None
    licensed_area: str = ''

    def __post_init__(self):
        self.aggregate_type = 'ExploitationLicense'
        self.event_type = 'ExploitationLicenseIssued'
        super().__post_init__()

class ResourceMonitoringReportFiled(ComplianceEvent):
    """Emitted when resource monitoring report is filed."""
    report_id: UUID
    license_id: UUID
    reporting_period: str
    report_date: date
    quantity_extracted: str = ''
    environmental_impact: str = ''

    def __post_init__(self):
        self.aggregate_type = 'ResourceMonitoring'
        self.event_type = 'ResourceMonitoringReportFiled'
        super().__post_init__()

class ResourceLicenseStatusChanged(StatusChangeEvent):
    """Track resource license status (active, suspended, revoked)."""
    license_id: UUID
    reason: str = ''

    def __post_init__(self):
        self.aggregate_type = 'ExploitationLicense'
        self.event_type = 'ResourceLicenseStatusChanged'
        super().__post_init__()

class EnvironmentalImpactAssessmentApproved(ComplianceEvent):
    """Emitted when EIA is approved for resource project."""
    assessment_id: UUID
    project_id: UUID
    approval_date: date
    approved_by: str = ''
    mitigation_measures: str = ''

    def __post_init__(self):
        self.aggregate_type = 'EnvironmentalAssessment'
        self.event_type = 'EnvironmentalImpactAssessmentApproved'
        super().__post_init__()