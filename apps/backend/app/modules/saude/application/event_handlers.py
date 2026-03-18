"""
Saúde (Health) Module Event Handlers
Handlers that process health domain events.
"""
import logging
from typing import Awaitable, Callable
from apps.backend.app.core.events.domain_event import DomainEvent
from apps.backend.app.modules.saude.domain.events import HealthProviderRegistered, MedicalVisitRecorded, HealthVaccinationCompleted, HealthProviderStatusChanged, MedicalLicenseIssued
logger = logging.getLogger(__name__)

async def handle_health_provider_registered(event: HealthProviderRegistered) -> None:
    """Handler for HealthProviderRegistered events."""
    logger.info(f'Health provider {event.provider_name} registered')
    pass

async def handle_medical_visit_recorded(event: MedicalVisitRecorded) -> None:
    """Handler for MedicalVisitRecorded events."""
    logger.info(f'Medical visit recorded for patient {event.aggregate_id}')
    pass

async def handle_health_vaccination_completed(event: HealthVaccinationCompleted) -> None:
    """Handler for HealthVaccinationCompleted events (ACAO compliance)."""
    logger.info(f'Vaccination completed for patient {event.aggregate_id}')
    pass

async def handle_health_provider_status_changed(event: HealthProviderStatusChanged) -> None:
    """Handler for HealthProviderStatusChanged events."""
    logger.info(f'Provider status changed: {event.old_status} -> {event.new_status}')
    pass

async def handle_medical_license_issued(event: MedicalLicenseIssued) -> None:
    """Handler for MedicalLicenseIssued events (ACAO compliance)."""
    logger.info(f'License {event.license_number} issued for professional {event.aggregate_id}')
    pass
SAUDE_EVENT_HANDLERS: dict[str, Callable[[DomainEvent], Awaitable[None]]] = {'HealthProviderRegistered': handle_health_provider_registered, 'MedicalVisitRecorded': handle_medical_visit_recorded, 'HealthVaccinationCompleted': handle_health_vaccination_completed, 'HealthProviderStatusChanged': handle_health_provider_status_changed, 'MedicalLicenseIssued': handle_medical_license_issued}