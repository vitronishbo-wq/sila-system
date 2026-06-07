"""
Migration Service Module Command Handlers
Shows the pattern for migration/visa operations with event publishing.
"""

import logging
from datetime import UTC, date, datetime
from uuid import UUID

from apps.backend.app.core.events.event_bus import EventBus
from apps.backend.app.modules.migration_service.domain.events import (
    PassportIssued,
    VisaApplicationSubmitted,
    VisaApprovalDecided,
)

logger = logging.getLogger(__name__)


class SubmitVisaApplicationCommandHandler:
    """Submit visa application."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        application_id: UUID,
        applicant_id: UUID,
        visa_type: str,
        destination_country: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Submitting visa application for {visa_type}")
        try:
            event = VisaApplicationSubmitted(
                aggregate_id=application_id,
                aggregate_type="VisaApplication",
                event_type="VisaApplicationSubmitted",
                application_id=application_id,
                applicant_id=applicant_id,
                visa_type=visa_type,
                destination_country=destination_country,
                submission_date=date.today(),
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "SubmitVisaApplication",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Visa application submitted: {application_id}")
        except Exception as e:
            logger.error(f"Error submitting visa application: {e}")
            raise


class DecideVisaApprovalCommandHandler:
    """Decide visa approval (ACAO compliance)."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        decision_id: UUID,
        application_id: UUID,
        approved: bool,
        decision_made_by: str = "",
        validity_period_days: int | None = None,
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Processing visa approval decision {decision_id}")
        try:
            event = VisaApprovalDecided(
                aggregate_id=decision_id,
                aggregate_type="VisaApproval",
                event_type="VisaApprovalDecided",
                decision_id=decision_id,
                application_id=application_id,
                approved=approved,
                decision_date=date.today(),
                decision_made_by=decision_made_by,
                validity_period_days=validity_period_days,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "DecideVisaApproval",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Visa approval decided: {decision_id}")
        except Exception as e:
            logger.error(f"Error deciding visa approval: {e}")
            raise


class IssuePassportCommandHandler:
    """Issue passport (ACAO compliance)."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        passport_id: UUID,
        citizen_id: UUID,
        passport_number: str,
        expiry_date: date,
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Issuing passport {passport_number}")
        try:
            event = PassportIssued(
                aggregate_id=passport_id,
                aggregate_type="Passport",
                event_type="PassportIssued",
                passport_id=passport_id,
                citizen_id=citizen_id,
                passport_number=passport_number,
                issue_date=date.today(),
                expiry_date=expiry_date,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "IssuePassport",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Passport issued: {passport_number}")
        except Exception as e:
            logger.error(f"Error issuing passport: {e}")
            raise
