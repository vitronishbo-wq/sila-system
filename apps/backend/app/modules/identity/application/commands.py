"""
Identity Module Command Handlers
Shows the pattern for integrating event publishing in command handlers.
"""
import logging
from uuid import UUID
from datetime import date, datetime, timezone
from typing import Optional
from apps.backend.app.core.events.event_bus import EventBus
from apps.backend.app.modules.identity.domain.events import IdentityDocumentRequested, IdentityDocumentVerified, BiometricDataEnrolled
logger = logging.getLogger(__name__)

class RequestIdentityDocumentCommandHandler:
    """Request identity document."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(self, citizen_id: UUID, document_type: str, request_reason: str='', correlation_id: Optional[UUID]=None, user_id: Optional[UUID]=None) -> None:
        logger.info(f'Requesting {document_type} for citizen {citizen_id}')
        try:
            event = IdentityDocumentRequested(aggregate_id=citizen_id, aggregate_type='IdentityDocument', event_type='IdentityDocumentRequested', citizen_id=citizen_id, document_type=document_type, request_reason=request_reason, correlation_id=correlation_id, metadata={'user_id': str(user_id) if user_id else None, 'command_name': 'RequestIdentityDocument', 'timestamp_utc': datetime.now(timezone.utc).isoformat()})
            await self.event_bus.publish(event)
            logger.info(f'Identity document request published for {citizen_id}')
        except Exception as e:
            logger.error(f'Error requesting identity document: {e}')
            raise

class VerifyIdentityDocumentCommandHandler:
    """Verify identity document (ACAO compliance)."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(self, document_id: UUID, citizen_id: UUID, verification_level: str, verified_by: str='', correlation_id: Optional[UUID]=None, user_id: Optional[UUID]=None) -> None:
        logger.info(f'Verifying identity document {document_id}')
        try:
            event = IdentityDocumentVerified(aggregate_id=document_id, aggregate_type='IdentityDocument', event_type='IdentityDocumentVerified', citizen_id=citizen_id, verification_level=verification_level, verified_by=verified_by, verification_date=date.today(), correlation_id=correlation_id, metadata={'user_id': str(user_id) if user_id else None, 'command_name': 'VerifyIdentityDocument', 'timestamp_utc': datetime.now(timezone.utc).isoformat()})
            await self.event_bus.publish(event)
            logger.info(f'Identity verification published for {document_id}')
        except Exception as e:
            logger.error(f'Error verifying identity: {e}')
            raise

class EnrollBiometricDataCommandHandler:
    """Enroll biometric data for identity."""

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(self, citizen_id: UUID, biometric_type: str, enrolled_by: str='', correlation_id: Optional[UUID]=None, user_id: Optional[UUID]=None) -> None:
        logger.info(f'Enrolling {biometric_type} biometric for citizen {citizen_id}')
        try:
            event = BiometricDataEnrolled(aggregate_id=citizen_id, aggregate_type='BiometricData', event_type='BiometricDataEnrolled', citizen_id=citizen_id, biometric_type=biometric_type, enrollment_date=date.today(), enrolled_by=enrolled_by, correlation_id=correlation_id, metadata={'user_id': str(user_id) if user_id else None, 'command_name': 'EnrollBiometricData', 'timestamp_utc': datetime.now(timezone.utc).isoformat()})
            await self.event_bus.publish(event)
            logger.info(f'Biometric enrollment published for {citizen_id}')
        except Exception as e:
            logger.error(f'Error enrolling biometric: {e}')
            raise