"""
Justice Module Command Handlers with Event Publishing
Shows the pattern for integrating event publishing in command handlers.
"""

import logging
from datetime import UTC, date, datetime
from uuid import UUID

from apps.backend.app.core.events.event_bus import EventBus
from apps.backend.app.modules.justice.domain.events import (
    BirthRecordCertificateIssued,
    BirthRecordCreated,
    CitizenCreated,
    CitizenIdentityDocumentIssued,
)

logger = logging.getLogger(__name__)


class RegisterCitizenCommandHandler:
    """
    Command Handler Example: Register a new citizen.

    Pattern:
    1. Validate command
    2. Create or update aggregate
    3. Publish domain events
    4. Return result
    """

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
    ) -> None:
        """
        Handle citizen registration command.

        Args:
            citizen_id: Unique citizen ID
            first_name: First name
            last_name: Last name
            birth_date: Date of birth
            birth_place: Place of birth
            nationality: Nationality code
            correlation_id: For tracing related operations
            user_id: User performing the registration
        """
        logger.info(f"Handling RegisterCitizen command for {citizen_id}")
        try:
            citizen_created_event = CitizenCreated(
                aggregate_id=citizen_id,
                aggregate_type="Citizen",
                event_type="CitizenCreated",
                first_name=first_name,
                last_name=last_name,
                birth_date=birth_date,
                birth_place=birth_place,
                nationality=nationality,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "RegisterCitizen",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(citizen_created_event)
            logger.info(f"Successfully registered citizen {citizen_id}")
        except Exception as e:
            logger.error(f"Error registering citizen: {e}")
            raise


class IssueIdentityDocumentCommandHandler:
    """
    Command Handler Example: Issue identity document.

    This demonstrates ACAO compliance requirements for status tracking.
    """

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
    ) -> None:
        """
        Handle identity document issuance.

        ACAO Compliance:
        - Records official document issuance
        - Registers in compliance audit trail
        - Publishes to external systems
        """
        logger.info(f"Handling IssueIdentityDocument command for citizen {citizen_id}")
        try:
            document_issued_event = CitizenIdentityDocumentIssued(
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
                    "command_name": "IssueIdentityDocument",
                    "compliance_requirement": "ACAO",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(document_issued_event)
            logger.info(f"Identity document {document_number} issued for citizen {citizen_id}")
        except Exception as e:
            logger.error(f"Error issuing identity document: {e}")
            raise


class RegisterBirthRecordCommandHandler:
    """Command Handler Example: Register birth record."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        record_id: UUID,
        child_name: str,
        birth_date: date,
        birth_place: str,
        father_id: UUID | None = None,
        mother_id: UUID | None = None,
        registering_authority: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        """Handle birth record registration."""
        logger.info(f"Handling RegisterBirthRecord command for {record_id}")
        try:
            birth_record_event = BirthRecordCreated(
                aggregate_id=record_id,
                aggregate_type="BirthRecord",
                event_type="BirthRecordCreated",
                child_name=child_name,
                birth_date=birth_date,
                birth_place=birth_place,
                father_id=father_id,
                mother_id=mother_id,
                registering_authority=registering_authority,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(birth_record_event)
            logger.info(f"Birth record {record_id} registered")
        except Exception as e:
            logger.error(f"Error registering birth record: {e}")
            raise


class IssueBirthCertificateCommandHandler:
    """Command Handler Example: Issue birth certificate (ACAO compliance)."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        record_id: UUID,
        certificate_number: str,
        issued_date: date,
        serial_number: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        """Handle birth certificate issuance."""
        logger.info(f"Handling IssueBirthCertificate command for record {record_id}")
        try:
            certificate_event = BirthRecordCertificateIssued(
                aggregate_id=record_id,
                aggregate_type="BirthRecord",
                event_type="BirthRecordCertificateIssued",
                certificate_number=certificate_number,
                issued_date=issued_date,
                serial_number=serial_number,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "compliance_requirement": "ACAO",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(certificate_event)
            logger.info(f"Birth certificate {certificate_number} issued for record {record_id}")
        except Exception as e:
            logger.error(f"Error issuing birth certificate: {e}")
            raise
