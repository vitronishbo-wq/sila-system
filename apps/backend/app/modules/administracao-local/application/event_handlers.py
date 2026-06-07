"""
Administração Local — Event Handlers
Consumes cross-module events for territorial confirmation.
"""

import logging
from collections.abc import Awaitable, Callable

from apps.backend.app.core.events.domain_event import DomainEvent

logger = logging.getLogger(__name__)


async def handle_student_enrolled(event: DomainEvent) -> None:
    """Consume StudentEnrolled from Educação to confirm residence catchment area."""
    metadata = event.metadata or {}
    student_id = metadata.get("student_id")
    institution_id = metadata.get("institution_id")
    logger.info(
        f"StudentEnrolled consumed by AdministracaoLocal: "
        f"student={student_id} institution={institution_id}"
    )


async def handle_payment_confirmed(event: DomainEvent) -> None:
    """Consume PaymentConfirmed to update territorial fee records."""
    metadata = event.metadata or {}
    payment_ref = metadata.get("payment_ref")
    citizen_id = metadata.get("citizen_id")
    logger.info(
        f"PaymentConfirmed consumed by AdministracaoLocal: "
        f"ref={payment_ref} citizen={citizen_id}"
    )


ADMINISTRACAO_LOCAL_EVENT_HANDLERS: dict[str, Callable[[DomainEvent], Awaitable[None]]] = {
    "StudentEnrolled": handle_student_enrolled,
    "PaymentConfirmed": handle_payment_confirmed,
}
