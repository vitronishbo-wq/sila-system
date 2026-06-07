"""
Economy Module Domain Events
ACAO Compliance: All events track financial transactions and economic status.
"""

from datetime import date
from decimal import Decimal
from typing import Optional
from uuid import UUID

from apps.backend.app.core.events.domain_event import (
    AuditableEvent,
    ComplianceEvent,
    DomainEvent,
    StatusChangeEvent,
)


class EconomicAgentRegistered(AuditableEvent):
    """Emitted when an economic agent (business/enterprise) is registered."""

    agent_id: UUID
    agent_name: str
    agent_type: str
    registration_number: str = ""
    sector: str = ""

    def __post_init__(self):
        self.aggregate_type = "EconomicAgent"
        self.event_type = "EconomicAgentRegistered"
        super().__post_init__()


class EconomicActivityStarted(ComplianceEvent):
    """Emitted when economic activity begins (ACAO compliance)."""

    agent_id: UUID
    activity_code: str
    activity_description: str
    start_date: date
    registered_by: str = ""

    def __post_init__(self):
        self.aggregate_type = "EconomicActivity"
        self.event_type = "EconomicActivityStarted"
        super().__post_init__()


class EconomicAgentStatusChanged(StatusChangeEvent):
    """Track economic agent status transitions (active, suspended, closed)."""

    agent_id: UUID
    reason: str = ""

    def __post_init__(self):
        self.aggregate_type = "EconomicAgent"
        self.event_type = "EconomicAgentStatusChanged"
        super().__post_init__()


class TaxRegistrationIssued(ComplianceEvent):
    """Emitted when tax registration is issued (ACAO requirement)."""

    tax_id: str
    agent_id: UUID
    issue_date: date
    effective_date: date
    tax_authority: str = ""

    def __post_init__(self):
        self.aggregate_type = "TaxRegistration"
        self.event_type = "TaxRegistrationIssued"
        super().__post_init__()


class EconomicLicenseObtained(ComplianceEvent):
    """Emitted when business license is obtained."""

    license_number: str
    agent_id: UUID
    license_type: str
    issue_date: date
    expiry_date: date | None = None
    issuing_authority: str = ""

    def __post_init__(self):
        self.aggregate_type = "EconomicLicense"
        self.event_type = "EconomicLicenseObtained"
        super().__post_init__()
