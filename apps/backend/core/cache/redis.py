from config.settings import settings
from redis.asyncio import from_url

# Initialize Redis client using settings
redis_client = from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)

__all__ = ["redis_client"]
