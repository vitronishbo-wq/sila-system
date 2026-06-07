"""Redis message broker for pub/sub event distribution."""

import json
from collections.abc import AsyncGenerator

import redis.asyncio as redis
from apps.backend.app.core.observability.enterprise_logging import get_logger
from apps.backend.app.core.settings import settings

logger = get_logger("core.events.broker")


class RedisBroker:
    """Redis-based pub/sub message broker for event distribution.

    Distributes events to multiple subscribers across service instances.
    Provides lossy delivery (no persistence) suitable for real-time notifications.

    For guaranteed delivery (audit trails), use database outbox pattern.

    Example:
        ```python
        broker = RedisBroker()

        # Publish
        await broker.publish("USER_LOGGED_IN", {"user_id": "123"})

        # Subscribe and consume
        async for message in broker.subscribe("USER_LOGGED_IN"):
            event = json.loads(message)
            await handler.handle(event)
        ```
    """

    def __init__(self):
        """Initialize Redis connection.

        Uses REDIS_URL from settings. Supports connection pooling.
        """
        try:
            self.client = redis.Redis.from_url(
                settings.REDIS_URL, decode_responses=True, auto_close_conn_pool=False
            )
        except Exception as e:
            logger.error("redis_broker_init_failed", extra={"error": str(e)})
            raise

    async def publish(self, channel: str, message: dict) -> int:
        """Publish message to channel.

        Args:
            channel: Channel name (e.g., "USER_LOGGED_IN")
            message: Message payload as dict

        Returns:
            Number of subscribers that received the message

        Raises:
            ConnectionError: If Redis is unavailable
        """
        try:
            message_json = json.dumps(message)
            subscribers_count = await self.client.publish(channel, message_json)
            logger.info(
                "event_published_redis",
                extra={"channel": channel, "subscribers": subscribers_count},
            )
            return subscribers_count
        except Exception as e:
            logger.error("redis_publish_failed", extra={"channel": channel, "error": str(e)})
            raise

    async def subscribe(self, channel: str) -> AsyncGenerator[str, None]:
        """Subscribe to channel and consume messages.

        Args:
            channel: Channel name to subscribe to

        Yields:
            JSON string of each message received

        Example:
            ```python
            async for message in broker.subscribe("USER_LOGGED_IN"):
                event = json.loads(message)
                print(event)
            ```
        """
        pubsub = self.client.pubsub()
        try:
            await pubsub.subscribe(channel)
            logger.info("subscribed_to_channel", extra={"channel": channel})
            async for msg in pubsub.listen():
                if msg["type"] == "message":
                    yield msg["data"]
        finally:
            await pubsub.close()

    async def health_check(self) -> bool:
        """Check if Redis connection is healthy.

        Returns:
            bool: True if connected, False otherwise
        """
        try:
            await self.client.ping()
            return True
        except Exception as e:
            logger.warning("redis_health_check_failed", extra={"error": str(e)})
            return False
