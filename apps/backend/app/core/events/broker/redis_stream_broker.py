"""Redis Streams Broker Implementation - Phase 19"""

import json
import logging
from collections.abc import AsyncIterator
from typing import Any

import redis.asyncio as redis

logger = logging.getLogger("events.broker")


class RedisStreamBroker:
    """Redis Streams broker for event publishing with guaranteed delivery"""

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.client = None

    async def connect(self):
        """Initialize Redis connection"""
        self.client = await redis.from_url(self.redis_url, decode_responses=True, encoding="utf-8")
        logger.info("Redis broker connected", extra={"url": self.redis_url})

    async def disconnect(self):
        """Close Redis connection"""
        if self.client:
            await self.client.close()

    async def publish(self, stream: str, message: dict[str, Any]) -> str:
        """Publish message to stream (guaranteed delivery)"""
        if not self.client:
            await self.connect()
        message_id = await self.client.xadd(stream, {"data": json.dumps(message, default=str)})
        logger.info("event_published", extra={"stream": stream, "message_id": message_id})
        return message_id

    async def create_consumer_group(self, stream: str, group: str, start_id: str = "0"):
        """Create consumer group for stream"""
        if not self.client:
            await self.connect()
        try:
            await self.client.xgroup_create(stream, group, id=start_id, mkstream=True)
            logger.info("consumer_group_created", extra={"stream": stream, "group": group})
        except redis.ResponseError as e:
            if "BUSYGROUP" not in str(e):
                raise
            logger.info("consumer_group_exists", extra={"stream": stream, "group": group})

    async def read(
        self, stream: str, group: str, consumer: str, block_ms: int = 5000, count: int = 10
    ) -> AsyncIterator[tuple[str, dict[str, Any]]]:
        """Read messages from consumer group (infinite stream)"""
        if not self.client:
            await self.connect()
        await self.create_consumer_group(stream, group)
        while True:
            try:
                messages = await self.client.xreadgroup(
                    group, consumer, {stream: ">"}, count=count, block=block_ms
                )
                for _stream_name, events in messages or []:
                    for event_id, data in events:
                        payload = json.loads(data.get("data", "{}"))
                        yield (event_id, payload)
            except Exception as e:
                logger.error("broker_read_error", extra={"error": str(e)})
                await asyncio.sleep(1)

    async def acknowledge(self, stream: str, group: str, message_id: str):
        """Acknowledge message in consumer group"""
        if not self.client:
            await self.connect()
        await self.client.xack(stream, group, message_id)
