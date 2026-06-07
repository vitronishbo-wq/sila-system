"""Compliance domain commands."""

from dataclasses import dataclass


@dataclass
class LogAuditCommand:
    """Command to log audit action."""

    entity_type: str
    entity_id: str
    action: str
    details: dict


@dataclass
class LogComplianceEventCommand:
    """Command to log compliance event."""

    event_name: str
    event_data: dict
    severity: str = "INFO"


@dataclass
class CreateComplianceCheckCommand:
    """Command to create compliance check."""

    check_name: str
    target_id: str
    rules: dict
    metadata: dict | None = None
