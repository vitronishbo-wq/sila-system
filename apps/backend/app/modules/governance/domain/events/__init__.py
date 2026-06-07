"""
Governance Module Domain Events
ACAO Compliance: All events track government decisions and administrative actions.
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


class GovernmentDecisionMade(AuditableEvent):
    """Emitted when a government decision is made."""

    decision_id: UUID
    decision_title: str
    decision_date: date
    decision_type: str
    decision_maker: str = ""
    affected_area: str = ""

    def __post_init__(self):
        self.aggregate_type = "GovernmentDecision"
        self.event_type = "GovernmentDecisionMade"
        super().__post_init__()


class PolicyPublished(ComplianceEvent):
    """Emitted when government policy is published (ACAO compliance)."""

    policy_id: UUID
    policy_number: str
    policy_name: str
    publication_date: date
    effective_date: date
    published_by: str = ""

    def __post_init__(self):
        self.aggregate_type = "GovernmentPolicy"
        self.event_type = "PolicyPublished"
        super().__post_init__()


class AdminOfficeStatusChanged(StatusChangeEvent):
    """Track administrative office status transitions."""

    office_id: UUID
    office_name: str
    location: str = ""

    def __post_init__(self):
        self.aggregate_type = "AdminOffice"
        self.event_type = "AdminOfficeStatusChanged"
        super().__post_init__()


class PublicServiceApproved(ComplianceEvent):
    """Emitted when public service is approved for operation."""

    service_id: UUID
    service_name: str
    approval_date: date
    approval_authority: str = ""
    service_type: str = ""

    def __post_init__(self):
        self.aggregate_type = "PublicService"
        self.event_type = "PublicServiceApproved"
        super().__post_init__()


class OfficialRequiredActionIssued(ComplianceEvent):
    """Emitted when an official action is issued requiring compliance."""

    action_id: UUID
    action_type: str
    issue_date: date
    deadline: date | None = None
    issued_by: str = ""

    def __post_init__(self):
        self.aggregate_type = "OfficialAction"
        self.event_type = "OfficialRequiredActionIssued"
        super().__post_init__()
