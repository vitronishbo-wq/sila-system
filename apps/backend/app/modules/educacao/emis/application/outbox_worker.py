"""EMIS Outbox Worker — consumes EnrollmentCreated, TransferCompleted, InstitutionUpdated
from the core event_outbox and pushes data to EMIS.

Flow:
  OutboxRepository.get_unprocessed(limit=50)
  → filter events relevant to EMIS
  → EmisSyncEngine.push_*(entity_id)
  → OutboxRepository.mark_processed(event.id)
"""

from __future__ import annotations

import json
import logging
from uuid import UUID

from apps.backend.app.core.events.outbox.outbox_repository import OutboxRepository
from apps.backend.app.core.database.session import AsyncSessionLocal
from apps.backend.app.modules.educacao.emis.application.sync_engine import (
    EmisSyncEngine,
)

logger = logging.getLogger(__name__)

EMIS_EVENTS = {
    "enrollment_created",
    "enrollment_completed",
    "transfer_completed",
    "institution_updated",
    "student_enrolled",
}


async def process_emis_outbox(batch_size: int = 50) -> dict[str, int]:
    """Poll outbox for EMIS-relevant events, sync to EMIS, mark processed."""
    async with AsyncSessionLocal() as session:
        outbox_repo = OutboxRepository(session)
        engine = EmisSyncEngine(session=session)

        events = await outbox_repo.get_unprocessed(limit=batch_size)
        emis_events = [e for e in events if e.event_name in EMIS_EVENTS]

        processed = 0
        skipped = 0
        failed = 0

        for event in emis_events:
            try:
                payload = event.payload
                if isinstance(payload, str):
                    payload = json.loads(payload)

                entity_id = payload.get("enrollment_id") or payload.get("transfer_id") or payload.get("institution_id") or payload.get("student_id")
                if not entity_id:
                    logger.warning("emis_outbox.no_entity_id event=%s id=%s", event.event_name, event.event_id)
                    skipped += 1
                    await outbox_repo.mark_processed(event.id)
                    continue

                uid = UUID(entity_id) if isinstance(entity_id, str) else entity_id

                if event.event_name in ("enrollment_created", "enrollment_completed", "student_enrolled"):
                    await engine.push_enrollment(uid)
                elif event.event_name == "transfer_completed":
                    await engine.push_enrollment(uid)
                elif event.event_name == "institution_updated":
                    await engine.push_institution(uid)

                await outbox_repo.mark_processed(event.id)
                processed += 1
                logger.info("emis_outbox.processed event=%s entity=%s", event.event_name, entity_id)

            except Exception as exc:
                logger.error("emis_outbox.failed event=%s error=%s", event.event_name, exc)
                failed += 1

        await session.commit()
        return {"processed": processed, "skipped": skipped, "failed": failed}
