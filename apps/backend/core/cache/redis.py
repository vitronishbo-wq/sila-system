from redis.asyncio import Redis, from_url
from config.settings import settings

# Initialize Redis client using settings
redis_client = from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True
)

__all__ = ["redis_client"]
