"""EMIS Celery tasks — periodic sync to external Education Management Information System."""

from __future__ import annotations

import logging

from apps.backend.app.core.celery import app as celery_app
from apps.backend.app.modules.educacao.emis.application.sync_engine import EmisSyncEngine
from apps.backend.app.modules.educacao.emis.application.outbox_worker import process_emis_outbox

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)
def emis_sync_enrollments(self):
    """Push recent enrollments to EMIS (runs every 5 minutes)."""
    import asyncio

    async def _run():
        engine = EmisSyncEngine()
        result = await engine.sync_all_pending_enrollments(limit=50)
        logger.info("emis_sync_enrollments.completed", extra=result)
        return result

    return asyncio.run(_run())


@celery_app.task(bind=True, max_retries=3, default_retry_delay=3600)
def emis_sync_institutions(self):
    """Push institutions to EMIS (runs daily)."""
    import asyncio

    async def _run():
        engine = EmisSyncEngine()
        result = await engine.sync_all_institutions(limit=200)
        logger.info("emis_sync_institutions.completed", extra=result)
        return result

    return asyncio.run(_run())


@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)
def emis_process_outbox(self):
    """Consume outbox events and push to EMIS (runs every 2 minutes)."""
    import asyncio

    async def _run():
        result = await process_emis_outbox(batch_size=50)
        logger.info("emis_process_outbox.completed", extra=result)
        return result

    return asyncio.run(_run())


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def emis_retry_dead_letter(self):
    """Reprocess RETRY and DEAD_LETTER entries (runs every 15 minutes)."""
    import asyncio
    from uuid import UUID

    from apps.backend.app.core.database.session import AsyncSessionLocal
    from apps.backend.app.modules.educacao.emis.application.sync_engine import (
        EmisSyncEngine,
        SyncLogRepository,
    )
    from apps.backend.app.modules.educacao.emis.domain.models import SyncStatus

    async def _run():
        async with AsyncSessionLocal() as session:
            repo = SyncLogRepository(session)
            engine = EmisSyncEngine(session=session)
            retryable = await repo.list_logs(status=SyncStatus.RETRY.value, limit=200)
            dead = await repo.list_logs(status=SyncStatus.DEAD_LETTER.value, limit=200)
            reprocessed = 0
            for entry in retryable + dead:
                try:
                    if entry.entity_type == "enrollment":
                        await engine.push_enrollment(UUID(entry.entity_id))
                    elif entry.entity_type == "student":
                        await engine.push_student(UUID(entry.entity_id))
                    elif entry.entity_type == "institution":
                        await engine.push_institution(UUID(entry.entity_id))
                    reprocessed += 1
                except Exception:
                    continue
            return {"reprocessed": reprocessed, "total": len(retryable) + len(dead)}

    return asyncio.run(_run())


# Register beat schedule
celery_app.conf.beat_schedule["emis-sync-enrollments-every-5min"] = {
    "task": "apps.backend.app.modules.educacao.emis.application.tasks.emis_sync_enrollments",
    "schedule": 300.0,
    "options": {"expires": 290},
}

celery_app.conf.beat_schedule["emis-sync-institutions-daily"] = {
    "task": "apps.backend.app.modules.educacao.emis.application.tasks.emis_sync_institutions",
    "schedule": 86400.0,
    "options": {"expires": 86300},
}

celery_app.conf.beat_schedule["emis-process-outbox-every-2min"] = {
    "task": "apps.backend.app.modules.educacao.emis.application.tasks.emis_process_outbox",
    "schedule": 120.0,
    "options": {"expires": 115},
}

celery_app.conf.beat_schedule["emis-retry-dead-letter-every-15min"] = {
    "task": "apps.backend.app.modules.educacao.emis.application.tasks.emis_retry_dead_letter",
    "schedule": 900.0,
    "options": {"expires": 890},
}
