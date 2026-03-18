"""
Civil Protection Module Command Handlers
Shows the pattern for civil protection operations with event publishing.
"""
import logging
from uuid import UUID
from datetime import date, datetime, timezone
from typing import Optional
from apps.backend.app.core.events.event_bus import EventBus
from apps.backend.app.modules.civil_protection.domain.events import EmergencyAlertIssued, DisasterEventOccurred, EvacuationInitiated
logger = logging.getLogger(__name__)

class IssueEmergencyAlertCommandHandler:
    """Issue emergency alert."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(self, alert_id: UUID, alert_level: str, alert_type: str, affected_area: str='', issued_by: str='', correlation_id: Optional[UUID]=None, user_id: Optional[UUID]=None) -> None:
        logger.info(f'Issuing emergency alert level {alert_level}')
        try:
            event = EmergencyAlertIssued(aggregate_id=alert_id, aggregate_type='EmergencyAlert', event_type='EmergencyAlertIssued', alert_id=alert_id, alert_level=alert_level, alert_type=alert_type, affected_area=affected_area, issued_at=datetime.now(timezone.utc), issued_by=issued_by, correlation_id=correlation_id, metadata={'user_id': str(user_id) if user_id else None, 'command_name': 'IssueEmergencyAlert', 'timestamp_utc': datetime.now(timezone.utc).isoformat()})
            await self.event_bus.publish(event)
            logger.info(f'Emergency alert issued: {alert_id}')
        except Exception as e:
            logger.error(f'Error issuing emergency alert: {e}')
            raise

class RecordDisasterEventCommandHandler:
    """Record disaster event."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(self, disaster_id: UUID, disaster_type: str, location: str, severity_level: str='', description: str='', correlation_id: Optional[UUID]=None, user_id: Optional[UUID]=None) -> None:
        logger.info(f'Recording disaster event: {disaster_type}')
        try:
            event = DisasterEventOccurred(aggregate_id=disaster_id, aggregate_type='DisasterEvent', event_type='DisasterEventOccurred', disaster_id=disaster_id, disaster_type=disaster_type, location=location, occurrence_date=date.today(), severity_level=severity_level, description=description, correlation_id=correlation_id, metadata={'user_id': str(user_id) if user_id else None, 'command_name': 'RecordDisasterEvent', 'timestamp_utc': datetime.now(timezone.utc).isoformat()})
            await self.event_bus.publish(event)
            logger.info(f'Disaster event recorded: {disaster_id}')
        except Exception as e:
            logger.error(f'Error recording disaster event: {e}')
            raise

class InitiateEvacuationCommandHandler:
    """Initiate evacuation (ACAO compliance)."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(self, evacuation_id: UUID, disaster_id: UUID, affected_population: int, evacuation_zone: str, initiated_by: str='', correlation_id: Optional[UUID]=None, user_id: Optional[UUID]=None) -> None:
        logger.info(f'Initiating evacuation for {affected_population} people')
        try:
            event = EvacuationInitiated(aggregate_id=evacuation_id, aggregate_type='Evacuation', event_type='EvacuationInitiated', evacuation_id=evacuation_id, disaster_id=disaster_id, affected_population=affected_population, evacuation_zone=evacuation_zone, initiated_date=date.today(), initiated_by=initiated_by, correlation_id=correlation_id, metadata={'user_id': str(user_id) if user_id else None, 'command_name': 'InitiateEvacuation', 'timestamp_utc': datetime.now(timezone.utc).isoformat()})
            await self.event_bus.publish(event)
            logger.info(f'Evacuation initiated: {evacuation_id}')
        except Exception as e:
            logger.error(f'Error initiating evacuation: {e}')
            raise