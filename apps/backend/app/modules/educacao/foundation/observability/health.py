from dataclasses import dataclass


@dataclass
class HealthStatus:
    name: str
    healthy: bool
    details: dict[str, object]


async def check_database() -> HealthStatus:
    from apps.backend.app.core.db import db as core_db

    ok = await core_db.health_check()
    return HealthStatus(name="database", healthy=ok, details={})


async def check_eventbus() -> HealthStatus:
    # Try a light query against the outbox table to ensure DB access for event publishing
    try:
        from apps.backend.app.core.db import db as core_db
        from apps.backend.app.core.events.outbox.outbox_repository import OutboxRepository

        async with core_db.session_factory() as session:
            repo = OutboxRepository(session)
            events = await repo.get_unprocessed(limit=1)
            return HealthStatus(name="eventbus", healthy=True, details={"pending": len(events)})
    except Exception as e:
        return HealthStatus(name="eventbus", healthy=False, details={"error": str(e)})


async def check_redis() -> HealthStatus:
    try:
        from apps.backend.app.core.cache.service import cache_service

        pong = await cache_service.redis.ping()
        return HealthStatus(name="redis", healthy=bool(pong), details={})
    except Exception as e:
        return HealthStatus(name="redis", healthy=False, details={"error": str(e)})
