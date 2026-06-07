"""
Saúde (Health) Module Command Handlers
Shows the pattern for health operations with event publishing.
"""

import logging
from datetime import UTC, date, datetime
from uuid import UUID

from apps.backend.app.core.events.event_bus import EventBus
from apps.backend.app.modules.saude.domain.events import (
    HealthProviderRegistered,
    HealthVaccinationCompleted,
    MedicalVisitRecorded,
)

logger = logging.getLogger(__name__)


class RegisterHealthProviderCommandHandler:
    """Register health provider."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        provider_id: UUID,
        provider_name: str,
        provider_type: str,
        location: str = "",
        registration_number: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Registering health provider {provider_name}")
        try:
            event = HealthProviderRegistered(
                aggregate_id=provider_id,
                aggregate_type="HealthProvider",
                event_type="HealthProviderRegistered",
                provider_id=provider_id,
                provider_name=provider_name,
                provider_type=provider_type,
                location=location,
                registration_number=registration_number,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "command_name": "RegisterHealthProvider",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Health provider registered: {provider_id}")
        except Exception as e:
            logger.error(f"Error registering health provider: {e}")
            raise


class RecordMedicalVisitCommandHandler:
    """Record medical visit."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        visit_id: UUID,
        patient_id: UUID,
        provider_id: UUID,
        diagnosis: str = "",
        treatment: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Recording medical visit for patient {patient_id}")
        try:
            event = MedicalVisitRecorded(
                aggregate_id=visit_id,
                aggregate_type="MedicalVisit",
                event_type="MedicalVisitRecorded",
                visit_id=visit_id,
                patient_id=patient_id,
                provider_id=provider_id,
                visit_date=date.today(),
                diagnosis=diagnosis,
                treatment=treatment,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "patient_id": str(patient_id),
                    "command_name": "RecordMedicalVisit",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Medical visit recorded: {visit_id}")
        except Exception as e:
            logger.error(f"Error recording medical visit: {e}")
            raise


class CompleteVaccinationCommandHandler:
    """Complete vaccination (ACAO compliance)."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(
        self,
        patient_id: UUID,
        vaccine_type: str,
        administered_by: str = "",
        certificate_number: str = "",
        correlation_id: UUID | None = None,
        user_id: UUID | None = None,
    ) -> None:
        logger.info(f"Completing vaccination {vaccine_type} for patient {patient_id}")
        try:
            event = HealthVaccinationCompleted(
                aggregate_id=patient_id,
                aggregate_type="Vaccination",
                event_type="HealthVaccinationCompleted",
                patient_id=patient_id,
                vaccine_type=vaccine_type,
                vaccine_date=date.today(),
                administered_by=administered_by,
                certificate_number=certificate_number,
                correlation_id=correlation_id,
                metadata={
                    "user_id": str(user_id) if user_id else None,
                    "patient_id": str(patient_id),
                    "command_name": "CompleteVaccination",
                    "timestamp_utc": datetime.now(UTC).isoformat(),
                },
            )
            await self.event_bus.publish(event)
            logger.info(f"Vaccination completed for patient {patient_id}")
        except Exception as e:
            logger.error(f"Error completing vaccination: {e}")
            raise
