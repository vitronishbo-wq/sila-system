"""
Tourism Module Command Handlers
Shows the pattern for tourism operations with event publishing.
"""

import logging
from datetime import UTC, date, datetime
from uuid import UUID

from apps.backend.app.core.events.event_bus import EventBus
from apps.backend.app.modules.tourism.domain.events import (
    TourismBusinessRegistered,
    TourismOperatingLicenseIssued,
    TourismQualityInspectionDone,
)

logger = logging.getLogger(__name__)


class RegisterTourismBusinessCommandHandler:
    """Register tourism business."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        business_id: UUID,
        business_name: str,
        business_type: str,
        location: str = "",
        contact_info: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Registering tourism business {business_name}")
        try:
            event = TourismBusinessRegistered(
                aggregate_id=business_id,
                aggregate_type="TourismBusiness",
                event_type="TourismBusinessRegistered",
                business_id=business_id,
                business_name=business_name,
                business_type=business_type,
                location=location,
                registration_date=date.today(),
                contact_info=contact_info,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "RegisterTourismBusiness",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Tourism business registered: {business_id}")
        except Exception as e:
            logger.error(f"Error registering tourism business: {e}")
            raise


class IssueTourismOperatingLicenseCommandHandler:
    """Issue tourism operating license (ACAO compliance)."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        license_id: UUID,
        business_id: UUID,
        license_number: str,
        expiry_date: date | None = None,
        license_category: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Issuing tourism operating license {license_number}")
        try:
            event = TourismOperatingLicenseIssued(
                aggregate_id=license_id,
                aggregate_type="TourismLicense",
                event_type="TourismOperatingLicenseIssued",
                license_id=license_id,
                business_id=business_id,
                license_number=license_number,
                issue_date=date.today(),
                expiry_date=expiry_date,
                license_category=license_category,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "IssueTourismOperatingLicense",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Tourism operating license issued: {license_number}")
        except Exception as e:
            logger.error(f"Error issuing tourism operating license: {e}")
            raise


class ConductTourismQualityInspectionCommandHandler:
    """Conduct tourism quality inspection (ACAO compliance)."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        inspection_id: UUID,
        business_id: UUID,
        inspector_id: str = "",
        quality_rating: str = "good",
        findings: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Conducting tourism quality inspection {inspection_id}")
        try:
            event = TourismQualityInspectionDone(
                aggregate_id=inspection_id,
                aggregate_type="TourismInspection",
                event_type="TourismQualityInspectionDone",
                inspection_id=inspection_id,
                business_id=business_id,
                inspection_date=date.today(),
                inspector_id=inspector_id,
                quality_rating=quality_rating,
                findings=findings,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "ConductTourismQualityInspection",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Tourism quality inspection done: {inspection_id}")
        except Exception as e:
            logger.error(f"Error conducting tourism inspection: {e}")
            raise
