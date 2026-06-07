"""ReservationExpirationJob — expires stale reservations and releases capacity."""

from __future__ import annotations

import logging

from apps.backend.app.core.celery import app as celery_app
from apps.backend.app.core.database.session import AsyncSessionLocal
from apps.backend.app.modules.educacao.application.marketplace.marketplace_service import (
    SeatReservationService,
)
from apps.backend.app.modules.educacao.infrastructure.repositories.marketplace_vacancy_repository import (
    MarketplaceVacancyRepository,
)
from apps.backend.app.modules.educacao.infrastructure.repositories.seat_reservation_repository import (
    SeatReservationRepository,
)

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=10)
def expire_stale_reservations(self):
    """Expires all PENDING reservations past their expires_at and releases capacity."""
    import asyncio

    async def _run():
        async with AsyncSessionLocal() as session:
            reservation_repo = SeatReservationRepository(session)
            vacancy_repo = MarketplaceVacancyRepository(session)
            service = SeatReservationService(reservation_repo, vacancy_repo)

            stale = await reservation_repo.expire_stale()
            if stale == 0:
                logger.info("reservation_sweeper.no_stale")
                return {"expired": 0}

            expired_ids = await _get_expired_ids(session)
            released = 0
            for rid in expired_ids:
                ok = await service.expire_reservation(rid, request_id="sweeper")
                if ok:
                    released += 1

            await session.commit()
            logger.info("reservation_sweeper.done", extra={"expired": stale, "released": released})
            return {"expired": stale, "released": released}

    async def _get_expired_ids(session):
        from sqlalchemy import select
        from apps.backend.app.modules.educacao.infrastructure.models.seat_reservation_model import (
            ReservationStatus,
            SeatReservationModel,
        )
        from datetime import datetime, timezone

        now = datetime.now(timezone.utc)
        stmt = select(SeatReservationModel.id).where(
            SeatReservationModel.status == ReservationStatus.EXPIRED.value,
        )
        result = await session.execute(stmt)
        return list(result.scalars().all())

    return asyncio.run(_run())


# Register beat schedule
celery_app.conf.beat_schedule = {
    "expire-stale-reservations-every-minute": {
        "task": "apps.backend.app.modules.educacao.application.marketplace.tasks.reservation_sweeper.expire_stale_reservations",
        "schedule": 60.0,
        "options": {"expires": 55},
    },
}
