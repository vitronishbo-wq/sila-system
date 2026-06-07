import redis
from apps.backend.app.core.settings import settings
from fastapi import APIRouter
from sqlalchemy import text

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check for DB and Redis."""
    status = {"status": "healthy", "services": {}}

    # Check DB
    try:
        from sqlalchemy.ext.asyncio import create_async_engine

        engine = create_async_engine(settings.DATABASE_URL)
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        status["services"]["database"] = "ok"
    except Exception as e:
        status["services"]["database"] = f"error: {str(e)}"
        status["status"] = "unhealthy"

    # Check Redis (if configured)
    redis_url = settings.REDIS_URL
    if redis_url:
        try:
            r = redis.from_url(redis_url)
            r.ping()
            status["services"]["redis"] = "ok"
        except Exception as e:
            status["services"]["redis"] = f"error: {str(e)}"
            status["status"] = "unhealthy"

    return status
