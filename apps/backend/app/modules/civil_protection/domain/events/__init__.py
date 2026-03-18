"""
Civil Protection Module Domain Events
ACAO Compliance: All events track disaster management and emergency response.
"""
from uuid import UUID
from datetime import date, datetime
from typing import Optional
from apps.backend.app.core.events.domain_event import DomainEvent, AuditableEvent, ComplianceEvent, StatusChangeEvent

class EmergencyAlertIssued(AuditableEvent):
    """Emitted when an emergency alert is issued."""
    alert_id: UUID
    alert_level: str
    alert_type: str
    affected_area: str = ''
    issued_at: datetime = None
    issued_by: str = ''

    def __post_init__(self):
        self.aggregate_type = 'EmergencyAlert'
        self.event_type = 'EmergencyAlertIssued'
        super().__post_init__()

class DisasterEventOccurred(AuditableEvent):
    """Emitted when a disaster event occurs."""
    disaster_id: UUID
    disaster_type: str
    location: str
    occurrence_date: date
    severity_level: str = ''
    description: str = ''

    def __post_init__(self):
        self.aggregate_type = 'DisasterEvent'
        self.event_type = 'DisasterEventOccurred'
        super().__post_init__()

class EvacuationInitiated(ComplianceEvent):
    """Emitted when evacuation is initiated (ACAO compliance)."""
    evacuation_id: UUID
    disaster_id: UUID
    affected_population: int
    evacuation_zone: str
    initiated_date: date
    initiated_by: str = ''

    def __post_init__(self):
        self.aggregate_type = 'Evacuation'
        self.event_type = 'EvacuationInitiated'
        super().__post_init__()

class CivilProtectionResourceStatusChanged(StatusChangeEvent):
    """Track resource status (available, deployed, lost)."""
    resource_id: UUID
    resource_type: str
    location: str = ''

    def __post_init__(self):
        self.aggregate_type = 'CivilProtectionResource'
        self.event_type = 'CivilProtectionResourceStatusChanged'
        super().__post_init__()

class DisasterRecoveryInitiated(ComplianceEvent):
    """Emitted when disaster recovery process starts."""
    recovery_id: UUID
    disaster_id: UUID
    start_date: date
    recovery_plan: str = ''
    coordinator: str = ''

    def __post_init__(self):
        self.aggregate_type = 'DisasterRecovery'
        self.event_type = 'DisasterRecoveryInitiated'
        super().__post_init__()