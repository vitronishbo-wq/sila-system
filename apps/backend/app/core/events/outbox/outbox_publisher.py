"""Outbox Publisher - Phase 19"""

import logging
from typing import Any

from apps.backend.app.core.events.broker.redis_stream_broker import RedisStreamBroker

logger = logging.getLogger("events.outbox")


class OutboxPublisher:
    """Publisher for outbox events to Redis Streams"""

    def __init__(self, broker: RedisStreamBroker = None):
        self.broker = broker or RedisStreamBroker()

    async def publish(self, event_name: str, payload: dict[str, Any]) -> str:
        """Publish event from outbox to broker"""
        message_id = await self.broker.publish(stream=event_name, message=payload)
        logger.info(
            "outbox_event_published", extra={"event_name": event_name, "message_id": message_id}
        )
        return message_id
