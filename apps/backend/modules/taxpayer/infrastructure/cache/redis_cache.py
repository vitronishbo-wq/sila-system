"""Redis Cache implementation"""

from typing import Optional, Any, List, Dict
import json
import redis.asyncio as redis
from datetime import timedelta


class RedisCache:
    """Async Redis cache client"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis_url = redis_url
        self._client: Optional[redis.Redis] = None
    
    async def connect(self):
        """Connect to Redis"""
        self._client = await redis.from_url(self.redis_url, decode_responses=True)
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self._client:
            await self._client.close()
            self._client = None
    
    def _ensure_client(self):
        """Ensure client is connected"""
        if not self._client:
            raise RuntimeError("Cache not connected. Call connect() first.")
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        self._ensure_client()
        value = await self._client.get(key)
        if value is None:
            return None
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """Set value in cache"""
        self._ensure_client()
        serialized = json.dumps(value) if not isinstance(value, str) else value
        
        if ttl:
            return bool(await self._client.setex(key, ttl, serialized))
        else:
            return bool(await self._client.set(key, serialized))
    
    async def delete(self, key: str) -> int:
        """Delete key from cache"""
        self._ensure_client()
        return int(await self._client.delete(key))
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        self._ensure_client()
        return bool(await self._client.exists(key))
    
    async def get_many(self, keys: List[str]) -> Dict[str, Any]:
        """Get multiple values"""
        self._ensure_client()
        values = await self._client.mget(keys)
        result = {}
        for key, value in zip(keys, values):
            if value is not None:
                try:
                    result[key] = json.loads(value)
                except json.JSONDecodeError:
                    result[key] = value
        return result
    
    async def set_many(
        self,
        mapping: Dict[str, Any],
        ttl: Optional[int] = None
    ) -> bool:
        """Set multiple values"""
        self._ensure_client()
        serialized = {}
        for key, value in mapping.items():
            serialized[key] = json.dumps(value) if not isinstance(value, str) else value
        
        if ttl:
            for key, value in serialized.items():
                await self._client.setex(key, ttl, value)
        else:
            await self._client.mset(serialized)
        
        return True
    
    async def increment(self, key: str, amount: int = 1) -> int:
        """Increment counter"""
        self._ensure_client()
        return int(await self._client.incrby(key, amount))
    
    async def decrement(self, key: str, amount: int = 1) -> int:
        """Decrement counter"""
        self._ensure_client()
        return int(await self._client.decrby(key, amount))
    
    async def expire(self, key: str, ttl: int) -> bool:
        """Set expiration on key"""
        self._ensure_client()
        return bool(await self._client.expire(key, ttl))
    
    async def ttl(self, key: str) -> int:
        """Get remaining TTL in seconds"""
        self._ensure_client()
        return int(await self._client.ttl(key))
    
    async def push(self, key: str, *values: Any) -> int:
        """Push values to list"""
        self._ensure_client()
        serialized = [json.dumps(v) if not isinstance(v, str) else v for v in values]
        return int(await self._client.rpush(key, *serialized))
    
    async def pop(self, key: str) -> Optional[Any]:
        """Pop from list"""
        self._ensure_client()
        value = await self._client.lpop(key)
        if value is None:
            return None
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    
    async def list_range(self, key: str, start: int = 0, stop: int = -1) -> List[Any]:
        """Get range from list"""
        self._ensure_client()
        values = await self._client.lrange(key, start, stop)
        result = []
        for v in values:
            try:
                result.append(json.loads(v))
            except json.JSONDecodeError:
                result.append(v)
        return result
    
    async def hset(self, name: str, key: str, value: Any) -> int:
        """Set hash field"""
        self._ensure_client()
        serialized = json.dumps(value) if not isinstance(value, str) else value
        return int(await self._client.hset(name, key, serialized))
    
    async def hget(self, name: str, key: str) -> Optional[Any]:
        """Get hash field"""
        self._ensure_client()
        value = await self._client.hget(name, key)
        if value is None:
            return None
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    
    async def hgetall(self, name: str) -> Dict[str, Any]:
        """Get all hash fields"""
        self._ensure_client()
        values = await self._client.hgetall(name)
        result = {}
        for key, value in values.items():
            try:
                result[key] = json.loads(value)
            except json.JSONDecodeError:
                result[key] = value
        return result
    
    async def hdel(self, name: str, *keys: str) -> int:
        """Delete hash fields"""
        self._ensure_client()
        return int(await self._client.hdel(name, *keys))
    
    async def clear_prefix(self, prefix: str) -> int:
        """Delete all keys matching prefix pattern"""
        self._ensure_client()
        pattern = f"{prefix}*"
        keys = await self._client.keys(pattern)
        if keys:
            return int(await self._client.delete(*keys))
        return 0
    
    async def clear(self) -> bool:
        """Clear entire cache"""
        self._ensure_client()
        await self._client.flushdb()
        return True


# Singleton instance
_cache_instance: Optional[RedisCache] = None


async def get_cache() -> RedisCache:
    """Get cache instance"""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = RedisCache()
        await _cache_instance.connect()
    return _cache_instance


async def close_cache():
    """Close cache connection"""
    global _cache_instance
    if _cache_instance:
        await _cache_instance.disconnect()
        _cache_instance = None
