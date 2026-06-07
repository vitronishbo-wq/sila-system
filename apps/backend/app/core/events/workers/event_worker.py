"""Event Worker - consumes events from Redis Streams - Phase 19"""

import logging

from apps.backend.app.core.events.audit_chain.audit_ledger import AuditLedger
from apps.backend.app.core.events.broker.redis_stream_broker import RedisStreamBroker
from apps.backend.app.core.events.event_versioning.event_upcaster import EventUpcaster
from apps.backend.app.core.events.multi_region_replication.replication_manager import ReplicationManager
from apps.backend.app.core.events.orchestrator.saga_orchestrator import SagaOrchestrator
from apps.backend.app.core.events.projection.projection_manager import ProjectionManager
from apps.backend.app.core.events.registry.handler_registry import HandlerRegistry

logger = logging.getLogger("events.worker")
orchestrator = SagaOrchestrator()
replication = ReplicationManager()
audit = AuditLedger()


class EventWorker:
    """Worker that consumes events from Redis Streams and invokes handlers"""

    def __init__(
        self,
        stream_name: str,
        group_name: str,
        consumer_name: str,
        broker: RedisStreamBroker | None = None,
    ):
        self.stream_name = stream_name
        self.group_name = group_name
        self.consumer_name = consumer_name
        self.broker = broker or RedisStreamBroker()
        self.running = False

    async def start(self):
        """Start consuming events"""
        self.running = True
        await self.broker.connect()
        logger.info(
            "event_worker_started",
            extra={
                "stream": self.stream_name,
                "group": self.group_name,
                "consumer": self.consumer_name,
            },
        )
        try:
            async for event_id, payload in self.broker.read(
                self.stream_name, self.group_name, self.consumer_name
            ):
                if not self.running:
                    break
                await self._process_event(event_id, payload)
        except Exception as e:
            logger.error(f"Event worker error: {e}")
        finally:
            await self.stop()

    async def _process_event(self, event_id: str, payload: dict):
        """Process event and invoke registered handlers"""
        try:
            event = EventUpcaster.upcast(payload)
            if not isinstance(event, dict) and hasattr(event, "__dict__"):
                event_payload = event.__dict__
            else:
                event_payload = event
            if isinstance(event_payload, dict):
                event_name = event_payload.get("name")
            else:
                event_name = getattr(event_payload, "name", None)
            handlers = HandlerRegistry.get(event_name)
            if not handlers:
                logger.warning("no_handlers_for_event", extra={"event": event_name})
            for handler in handlers:
                try:
                    logger.info(
                        "invoking_handler",
                        extra={"event": event_name, "handler": handler.__class__.__name__},
                    )
                    await handler.handle(event_payload)
                except Exception as e:
                    logger.error(
                        "handler_error",
                        extra={
                            "event": event_name,
                            "handler": handler.__class__.__name__,
                            "error": str(e),
                        },
                    )
            audit.append(event_payload)
            await replication.replicate(event_payload)
            await ProjectionManager.apply(event_payload)
            await orchestrator.process(event_payload)
            await self.broker.acknowledge(self.stream_name, self.group_name, event_id)
        except Exception as e:
            logger.error("event_processing_error", extra={"error": str(e)})

    async def stop(self):
        """Stop consuming events"""
        self.running = False
        await self.broker.disconnect()
        logger.info("event_worker_stopped")
