"""Outbox Worker - publishes outbox events to Redis Streams - Phase 19"""

import asyncio
import logging

from apps.backend.app.core.events.broker.redis_stream_broker import RedisStreamBroker
from apps.backend.app.core.events.outbox.outbox_publisher import OutboxPublisher
from apps.backend.app.core.events.outbox.outbox_repository import OutboxRepository
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger("events.outbox_worker")


class OutboxWorker:
    """Worker that publishes events from outbox to Redis Streams"""

    def __init__(
        self, db: AsyncSession, broker: RedisStreamBroker | None = None, poll_interval: int = 1
    ):
        self.db = db
        self.outbox_repo = OutboxRepository(db)
        self.broker = broker or RedisStreamBroker()
        self.publisher = OutboxPublisher(self.broker)
        self.poll_interval = poll_interval
        self.running = False

    async def start(self):
        """Start publishing events from outbox"""
        self.running = True
        await self.broker.connect()
        logger.info("outbox_worker_started")
        try:
            while self.running:
                await self._process_batch()
                await asyncio.sleep(self.poll_interval)
        except Exception as e:
            logger.error(f"Outbox worker error: {e}")
        finally:
            await self.stop()

    async def _process_batch(self):
        """Process batch of unprocessed events"""
        try:
            events = await self.outbox_repo.get_unprocessed(limit=100)
            if not events:
                return
            logger.info(f"Processing {len(events)} outbox events")
            for event in events:
                try:
                    await self.publisher.publish(event.event_name, event.payload)
                    await self.outbox_repo.mark_processed(event.id)
                    logger.info(
                        "outbox_event_processed",
                        extra={"event": event.event_name, "event_id": event.event_id},
                    )
                except Exception as e:
                    logger.error(
                        "outbox_event_error",
                        extra={
                            "event": event.event_name,
                            "event_id": event.event_id,
                            "error": str(e),
                        },
                    )
        except Exception as e:
            logger.error(f"Batch processing error: {e}")

    async def cleanup_old_events(self, days_retention: int = 7):
        """Delete processed events older than retention period"""
        try:
            deleted_count = await self.outbox_repo.delete_processed(days_retention)
            logger.info(f"Cleaned up {deleted_count} old events")
        except Exception as e:
            logger.error(f"Cleanup error: {e}")

    async def stop(self):
        """Stop the worker"""
        self.running = False
        await self.broker.disconnect()
        logger.info("outbox_worker_stopped")
