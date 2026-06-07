"""
API Module Domain Events
ACAO Compliance: All events track API gateway operations and compliance.
"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from apps.backend.app.core.events.domain_event import (
    AuditableEvent,
    ComplianceEvent,
    DomainEvent,
    StatusChangeEvent,
)


class APIEndpointRegistered(AuditableEvent):
    """Emitted when API endpoint is registered."""

    endpoint_id: UUID
    endpoint_name: str
    endpoint_path: str
    registration_date: date = None
    service_owner: str = ""

    def __post_init__(self):
        self.aggregate_type = "APIEndpoint"
        self.event_type = "APIEndpointRegistered"
        super().__post_init__()


class APIAccessTokenIssued(ComplianceEvent):
    """Emitted when API access token is issued (ACAO compliance)."""

    token_id: UUID
    client_id: UUID
    issued_at: datetime = None
    issued_by: str = ""
    expiry_date: date | None = None
    scopes: str = ""

    def __post_init__(self):
        self.aggregate_type = "APIAccessToken"
        self.event_type = "APIAccessTokenIssued"
        super().__post_init__()


class APIRequestProcessed(ComplianceEvent):
    """Emitted when API request is successfully processed (audit trail)."""

    request_id: UUID
    endpoint_id: UUID
    processed_at: datetime = None
    client_id: UUID = None
    response_status: int = 0

    def __post_init__(self):
        self.aggregate_type = "APIRequest"
        self.event_type = "APIRequestProcessed"
        super().__post_init__()


class APIEndpointStatusChanged(StatusChangeEvent):
    """Track API endpoint status (registered, active, deprecated, removed)."""

    endpoint_id: UUID
    reason: str = ""

    def __post_init__(self):
        self.aggregate_type = "APIEndpoint"
        self.event_type = "APIEndpointStatusChanged"
        super().__post_init__()


class APISecurityPolicyEnforced(ComplianceEvent):
    """Emitted when API security policy is enforced."""

    policy_id: UUID
    endpoint_id: UUID
    enforcement_date: date
    policy_type: str = ""
    enforced_by: str = ""

    def __post_init__(self):
        self.aggregate_type = "APISecurityPolicy"
        self.event_type = "APISecurityPolicyEnforced"
        super().__post_init__()
