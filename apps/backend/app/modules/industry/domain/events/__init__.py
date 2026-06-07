"""
Industry Module Domain Events
ACAO Compliance: All events track industrial operations and oversight.
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


class IndustrialFacilityRegistered(AuditableEvent):
    """Emitted when industrial facility is registered."""

    facility_id: UUID
    facility_name: str
    facility_type: str
    location: str = ""
    registration_number: str = ""

    def __post_init__(self):
        self.aggregate_type = "IndustrialFacility"
        self.event_type = "IndustrialFacilityRegistered"
        super().__post_init__()


class EnvironmentalPermitIssued(ComplianceEvent):
    """Emitted when environmental permit is issued (ACAO compliance)."""

    permit_id: UUID
    facility_id: UUID
    permit_number: str
    issue_date: date
    expiry_date: date | None = None
    environmental_class: str = ""

    def __post_init__(self):
        self.aggregate_type = "EnvironmentalPermit"
        self.event_type = "EnvironmentalPermitIssued"
        super().__post_init__()


class SafetyInspectionConducted(ComplianceEvent):
    """Emitted when safety inspection is conducted."""

    inspection_id: UUID
    facility_id: UUID
    inspection_date: date
    inspector_id: str = ""
    violations_found: int = 0
    compliance_status: str = "pass"

    def __post_init__(self):
        self.aggregate_type = "SafetyInspection"
        self.event_type = "SafetyInspectionConducted"
        super().__post_init__()


class IndustrialFacilityStatusChanged(StatusChangeEvent):
    """Track industrial facility status (operational, suspended, closed)."""

    facility_id: UUID
    reason: str = ""

    def __post_init__(self):
        self.aggregate_type = "IndustrialFacility"
        self.event_type = "IndustrialFacilityStatusChanged"
        super().__post_init__()


class SafetyCertificationIssued(ComplianceEvent):
    """Emitted when safety certification is issued."""

    certification_id: UUID
    facility_id: UUID
    certificate_number: str
    issue_date: date
    expiry_date: date | None = None
    certification_level: str = ""

    def __post_init__(self):
        self.aggregate_type = "SafetyCertification"
        self.event_type = "SafetyCertificationIssued"
        super().__post_init__()
