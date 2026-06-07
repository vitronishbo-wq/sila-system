"""
Saúde (Health) Module Domain Events
ACAO Compliance: All events track health services and medical records.
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


class HealthProviderRegistered(AuditableEvent):
    """Emitted when a health provider (hospital, clinic) is registered."""

    provider_id: UUID
    provider_name: str
    provider_type: str
    location: str = ""
    registration_number: str = ""

    def __post_init__(self):
        self.aggregate_type = "HealthProvider"
        self.event_type = "HealthProviderRegistered"
        super().__post_init__()


class MedicalVisitRecorded(AuditableEvent):
    """Emitted when a medical visit is recorded."""

    visit_id: UUID
    patient_id: UUID
    provider_id: UUID
    visit_date: date
    diagnosis: str = ""
    treatment: str = ""

    def __post_init__(self):
        self.aggregate_type = "MedicalVisit"
        self.event_type = "MedicalVisitRecorded"
        super().__post_init__()


class HealthVaccinationCompleted(ComplianceEvent):
    """Emitted when vaccination is completed (ACAO health compliance)."""

    patient_id: UUID
    vaccine_type: str
    vaccine_date: date
    administered_by: str = ""
    next_dose_date: date | None = None
    certificate_number: str = ""

    def __post_init__(self):
        self.aggregate_type = "Vaccination"
        self.event_type = "HealthVaccinationCompleted"
        super().__post_init__()


class HealthProviderStatusChanged(StatusChangeEvent):
    """Track health provider status transitions (active, suspended, closed)."""

    provider_id: UUID
    reason: str = ""

    def __post_init__(self):
        self.aggregate_type = "HealthProvider"
        self.event_type = "HealthProviderStatusChanged"
        super().__post_init__()


class MedicalLicenseIssued(ComplianceEvent):
    """Emitted when medical professional license is issued."""

    professional_id: UUID
    license_number: str
    specialization: str
    issue_date: date
    expiry_date: date | None = None
    issuing_authority: str = ""

    def __post_init__(self):
        self.aggregate_type = "MedicalLicense"
        self.event_type = "MedicalLicenseIssued"
        super().__post_init__()
