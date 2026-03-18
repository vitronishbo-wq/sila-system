"""
X-Road Module Command Handlers
Shows the pattern for X-Road integration operations with event publishing.
"""
import logging
from uuid import UUID
from datetime import date, datetime, timezone
from typing import Optional
from apps.backend.app.core.events.event_bus import EventBus
from apps.backend.app.modules.xroad.domain.events import XRoadServiceRegistered, XRoadServiceAccessApproved, XRoadServiceInvokedSuccessfully
logger = logging.getLogger(__name__)

class RegisterXRoadServiceCommandHandler:
    """Register X-Road service."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(self, service_id: UUID, service_name: str, provider_id: str='', interface_version: str='v1', correlation_id: Optional[UUID]=None, user_id: Optional[UUID]=None) -> None:
        logger.info(f'Registering X-Road service {service_name}')
        try:
            event = XRoadServiceRegistered(aggregate_id=service_id, aggregate_type='XRoadService', event_type='XRoadServiceRegistered', service_id=service_id, service_name=service_name, provider_id=provider_id, registration_date=date.today(), interface_version=interface_version, correlation_id=correlation_id, metadata={'user_id': str(user_id) if user_id else None, 'command_name': 'RegisterXRoadService', 'timestamp_utc': datetime.now(timezone.utc).isoformat()})
            await self.event_bus.publish(event)
            logger.info(f'X-Road service registered: {service_id}')
        except Exception as e:
            logger.error(f'Error registering X-Road service: {e}')
            raise

class ApproveXRoadServiceAccessCommandHandler:
    """Approve X-Road service access (ACAO compliance)."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(self, approval_id: UUID, service_id: UUID, consumer_id: str='', approved_by: str='', access_level: str='full', correlation_id: Optional[UUID]=None, user_id: Optional[UUID]=None) -> None:
        logger.info(f'Approving X-Road service access {approval_id}')
        try:
            event = XRoadServiceAccessApproved(aggregate_id=approval_id, aggregate_type='XRoadServiceAccess', event_type='XRoadServiceAccessApproved', approval_id=approval_id, service_id=service_id, consumer_id=consumer_id, approval_date=date.today(), approved_by=approved_by, access_level=access_level, correlation_id=correlation_id, metadata={'user_id': str(user_id) if user_id else None, 'command_name': 'ApproveXRoadServiceAccess', 'timestamp_utc': datetime.now(timezone.utc).isoformat()})
            await self.event_bus.publish(event)
            logger.info(f'X-Road service access approved: {approval_id}')
        except Exception as e:
            logger.error(f'Error approving X-Road service access: {e}')
            raise

class InvokeXRoadServiceCommandHandler:
    """Invoke X-Road service successfully (ACAO tracking)."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(self, invocation_id: UUID, service_id: UUID, consumer_id: str='', request_parameters: str='', response_time_ms: int=0, correlation_id: Optional[UUID]=None, user_id: Optional[UUID]=None) -> None:
        logger.info(f'Invoking X-Road service {service_id}')
        try:
            event = XRoadServiceInvokedSuccessfully(aggregate_id=invocation_id, aggregate_type='XRoadServiceInvocation', event_type='XRoadServiceInvokedSuccessfully', invocation_id=invocation_id, service_id=service_id, consumer_id=consumer_id, invocation_date=datetime.now(timezone.utc), request_parameters=request_parameters, response_time_ms=response_time_ms, correlation_id=correlation_id, metadata={'user_id': str(user_id) if user_id else None, 'command_name': 'InvokeXRoadService', 'timestamp_utc': datetime.now(timezone.utc).isoformat()})
            await self.event_bus.publish(event)
            logger.info(f'X-Road service invoked: {invocation_id}')
        except Exception as e:
            logger.error(f'Error invoking X-Road service: {e}')
            raise