"""Compliance domain queries."""

from dataclasses import dataclass


@dataclass
class GetAuditTrailQuery:
    """Query to retrieve audit trail for entity."""

    entity_id: str
    limit: int = 100


@dataclass
class ListComplianceEventsQuery:
    """Query to list compliance events."""

    filter_by: dict = None
    limit: int = 100
    offset: int = 0


@dataclass
class GetComplianceCheckQuery:
    """Query to retrieve compliance check."""

    check_id: str
