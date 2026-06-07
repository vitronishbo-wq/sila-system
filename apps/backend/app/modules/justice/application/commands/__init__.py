"""
Justice Module Application Commands and Handlers
CQRS command handlers that create domain events
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional
from uuid import UUID

from apps.backend.app.core.events.event_bus import EventBus
from apps.backend.app.modules.justice.domain.events import (
    CitizenCreated,
    CitizenIdentityDocumentIssued,
)


@dataclass
class RegisterCitizenCommand:
    """Command to register a new citizen."""

    citizen_id: UUID
    first_name: str
    last_name: str
    birth_date: date
    birth_place: str
    nationality: str
    correlation_id: UUID | None = None
    user_id: UUID | None = None


class RegisterCitizenCommandHandler:
    """Handle citizen registration command."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        citizen_id: UUID,
        first_name: str,
        last_name: str,
        birth_date: date,
        birth_place: str,
        nationality: str,
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ):
        """Handle citizen registration and emit CitizenCreated event."""
        event = CitizenCreated(
            aggregate_id=citizen_id,
            aggregate_type="Citizen",
            event_type="CitizenCreated",
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            birth_place=birth_place,
            nationality=nationality,
            correlation_id=correlation_id,
            metadata={"user_id": str(user_id)} if user_id else {},
        )
        await self.event_bus.publish(event)
        return event


@dataclass
class IssueIdentityDocumentCommand:
    """Command to issue an identity document."""

    citizen_id: UUID
    document_number: str
    document_type: str
    issue_date: date
    expiry_date: date | None = None
    issuing_authority: str = ""
    correlation_id: UUID | None = None
    user_id: UUID | None = None


class IssueIdentityDocumentCommandHandler:
    """Handle identity document issuance command."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        citizen_id: UUID,
        document_number: str,
        document_type: str,
        issue_date: date,
        expiry_date: date | None = None,
        issuing_authority: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ):
        """Handle identity document issuance and emit event."""
        event = CitizenIdentityDocumentIssued(
            aggregate_id=citizen_id,
            aggregate_type="Citizen",
            event_type="CitizenIdentityDocumentIssued",
            document_number=document_number,
            document_type=document_type,
            issue_date=issue_date,
            expiry_date=expiry_date,
            issuing_authority=issuing_authority,
            correlation_id=correlation_id,
            metadata={
                "user_id": str(user_id) if user_id else None,
                "compliance_requirement": "ACAO_6.2",
            },
        )
        await self.event_bus.publish(event)
        return event


__all__ = [
    "RegisterCitizenCommand",
    "RegisterCitizenCommandHandler",
    "IssueIdentityDocumentCommand",
    "IssueIdentityDocumentCommandHandler",
]
