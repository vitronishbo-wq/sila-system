"""
Documents Module Event Handlers
Handlers that process document domain events.
"""

import logging
from collections.abc import Awaitable, Callable

from apps.backend.app.core.events.domain_event import DomainEvent
from apps.backend.app.modules.documents.domain.events import (
    DocumentArchived,
    DocumentAuthenticated,
    DocumentRegistered,
    DocumentStatusChanged,
    OfficialDocumentIssued,
)

logger = logging.getLogger(__name__)


async def handle_document_registered(event: DocumentRegistered) -> None:
    """Handler for DocumentRegistered events."""
    logger.info(f"Document registered: {event.title}")
    pass


async def handle_document_status_changed(event: DocumentStatusChanged) -> None:
    """Handler for DocumentStatusChanged events."""
    logger.info(f"Document status changed: {event.old_status} -> {event.new_status}")
    pass


async def handle_official_document_issued(event: OfficialDocumentIssued) -> None:
    """Handler for OfficialDocumentIssued events (ACAO compliance)."""
    logger.info(f"Official document {event.document_number} issued")
    pass


async def handle_document_authenticated(event: DocumentAuthenticated) -> None:
    """Handler for DocumentAuthenticated events (ACAO compliance)."""
    logger.info(f"Document {event.aggregate_id} authenticated")
    pass


async def handle_document_archived(event: DocumentArchived) -> None:
    """Handler for DocumentArchived events (ACAO compliance)."""
    logger.info(f"Document archived with retention period {event.aggregate_id}")
    pass


DOCUMENTS_EVENT_HANDLERS: dict[str, Callable[[DomainEvent], Awaitable[None]]] = {
    "DocumentRegistered": handle_document_registered,
    "DocumentStatusChanged": handle_document_status_changed,
    "OfficialDocumentIssued": handle_official_document_issued,
    "DocumentAuthenticated": handle_document_authenticated,
    "DocumentArchived": handle_document_archived,
}
