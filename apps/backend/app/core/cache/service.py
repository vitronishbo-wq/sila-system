import redis.asyncio as redis
from app.core.config import settings

class CacheService:

    def __init__(self):
        redis_url = getattr(settings, 'REDIS_URL', 'redis://localhost:6379/0')
        self.redis = redis.from_url(redis_url, decode_responses=True)

    async def set_permission(self, user_id: str, permissions: list):
        await self.redis.set(f'perm:{user_id}', ','.join(permissions), ex=900)

    async def get_permissions(self, user_id: str):
        data = await self.redis.get(f'perm:{user_id}')
        return data.split(',') if data else None
cache_service = CacheService()