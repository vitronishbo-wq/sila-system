"""
Identity Module Event Handlers
Handlers that process identity domain events.
"""

import logging
from collections.abc import Awaitable, Callable

from apps.backend.app.core.events.domain_event import DomainEvent
from apps.backend.app.modules.identity.domain.events import (
    BiometricDataEnrolled,
    IdentityCredentialIssued,
    IdentityDocumentRequested,
    IdentityDocumentStatusChanged,
    IdentityDocumentVerified,
)

logger = logging.getLogger(__name__)


async def handle_identity_document_requested(event: IdentityDocumentRequested) -> None:
    """Handler for IdentityDocumentRequested events."""
    logger.info(f"Identity document requested for citizen {event.aggregate_id}")


async def handle_identity_document_verified(event: IdentityDocumentVerified) -> None:
    """Handler for IdentityDocumentVerified events (ACAO compliance)."""
    logger.info(f"Identity verified for citizen {event.aggregate_id}")


async def handle_identity_document_status_changed(event: IdentityDocumentStatusChanged) -> None:
    """Handler for IdentityDocumentStatusChanged events."""
    logger.info(
        f"Status changed for document {event.aggregate_id}: {event.old_status} -> {event.new_status}"
    )


async def handle_biometric_data_enrolled(event: BiometricDataEnrolled) -> None:
    """Handler for BiometricDataEnrolled events."""
    logger.info(f"Biometric data enrolled for citizen {event.aggregate_id}")


async def handle_identity_credential_issued(event: IdentityCredentialIssued) -> None:
    """Handler for IdentityCredentialIssued events (ACAO compliance)."""
    logger.info(f"Credential {event.credential_number} issued for {event.aggregate_id}")


async def handle_student_enrolled(event: DomainEvent) -> None:
    """Consume StudentEnrolled from Educação to update citizen's education record."""
    metadata = event.metadata or {}
    student_id = metadata.get("student_id")
    institution_id = metadata.get("institution_id")
    logger.info(
        f"StudentEnrolled consumed by Identity: student={student_id} "
        f"institution={institution_id}"
    )


IDENTITY_EVENT_HANDLERS: dict[str, Callable[[DomainEvent], Awaitable[None]]] = {
    "IdentityDocumentRequested": handle_identity_document_requested,
    "IdentityDocumentVerified": handle_identity_document_verified,
    "IdentityDocumentStatusChanged": handle_identity_document_status_changed,
    "BiometricDataEnrolled": handle_biometric_data_enrolled,
    "IdentityCredentialIssued": handle_identity_credential_issued,
    "StudentEnrolled": handle_student_enrolled,
}
