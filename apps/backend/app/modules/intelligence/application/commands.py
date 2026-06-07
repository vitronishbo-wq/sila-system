"""
Intelligence Module Command Handlers
Shows the pattern for intelligence operations with event publishing.
"""

import logging
from datetime import UTC, date, datetime
from uuid import UUID

from apps.backend.app.core.events.event_bus import EventBus
from apps.backend.app.modules.intelligence.domain.events import (
    IntelligenceAccessAuthorized,
    IntelligenceInformationClassified,
    IntelligenceReportSubmitted,
)

logger = logging.getLogger(__name__)


class SubmitIntelligenceReportCommandHandler:
    """Submit intelligence report."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        report_id: UUID,
        submitted_by: str = "",
        classification_level: str = "secret",
        subject: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Submitting intelligence report {report_id}")
        try:
            event = IntelligenceReportSubmitted(
                aggregate_id=report_id,
                aggregate_type="IntelligenceReport",
                event_type="IntelligenceReportSubmitted",
                report_id=report_id,
                submitted_at=datetime.now(UTC),
                submitted_by=submitted_by,
                classification_level=classification_level,
                subject=subject,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "SubmitIntelligenceReport",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Intelligence report submitted: {report_id}")
        except Exception as e:
            logger.error(f"Error submitting intelligence report: {e}")
            raise


class ClassifyIntelligenceCommandHandler:
    """Classify intelligence information (ACAO compliance)."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        classification_id: UUID,
        report_id: UUID,
        classification_level: str,
        classified_by: str = "",
        classification_authority: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Classifying intelligence information {classification_id}")
        try:
            event = IntelligenceInformationClassified(
                aggregate_id=classification_id,
                aggregate_type="IntelligenceClassification",
                event_type="IntelligenceInformationClassified",
                classification_id=classification_id,
                report_id=report_id,
                classification_date=date.today(),
                classification_level=classification_level,
                classified_by=classified_by,
                classification_authority=classification_authority,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "ClassifyIntelligence",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Intelligence classified: {classification_id}")
        except Exception as e:
            logger.error(f"Error classifying intelligence: {e}")
            raise


class AuthorizeIntelligenceAccessCommandHandler:
    """Authorize intelligence access (ACAO compliance)."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        authorization_id: UUID,
        report_id: UUID,
        authorized_personnel_id: UUID,
        access_level: str = "",
        expiry_date: date | None = None,
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Authorizing intelligence access {authorization_id}")
        try:
            event = IntelligenceAccessAuthorized(
                aggregate_id=authorization_id,
                aggregate_type="IntelligenceAccess",
                event_type="IntelligenceAccessAuthorized",
                authorization_id=authorization_id,
                report_id=report_id,
                authorized_personnel_id=authorized_personnel_id,
                authorization_date=date.today(),
                access_level=access_level,
                expiry_date=expiry_date,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "AuthorizeIntelligenceAccess",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Intelligence access authorized: {authorization_id}")
        except Exception as e:
            logger.error(f"Error authorizing intelligence access: {e}")
            raise
