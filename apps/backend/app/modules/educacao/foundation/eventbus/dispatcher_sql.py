from __future__ import annotations

import logging
import os
import uuid

from .adapters import kafka as kafka_adapter, rabbitmq as rabbit_adapter
from .sql.repository import OutboxRepository, ensure_schema, get_engine

logger = logging.getLogger(__name__)


class SQLOutboxDispatcher:
    def __init__(self, repo: OutboxRepository | None = None, worker_id: str | None = None, bus=None):
        engine = get_engine()
        ensure_schema(engine)
        self.repo = repo or OutboxRepository(engine=engine)
        self.worker_id = worker_id or f"worker-{uuid.uuid4()}"
        self.bus = bus or self._build_bus(os.getenv("OUTBOX_BUS", "local"))

    def _build_bus(self, bus_type: str):
        bt = (bus_type or "").lower()
        if bt in ("rabbit", "rabbitmq"):
            return rabbit_adapter.RabbitMQEventBus()
        if bt == "kafka":
            return kafka_adapter.KafkaEventBus()
        # local simple logger bus
        class _Local:
            def publish(self, topic, event):
                logger.info("publish %s %s", topic, event)

        return _Local()

    def run_once(self, batch: int = 50) -> dict[str, int]:
        events = self.repo.claim_events(self.worker_id, limit=batch)
        if not events:
            return {"claimed": 0, "sent": 0, "failed": 0}

        sent_ids: list[int] = []
        failed_count = 0
        for ev in events:
            try:
                self.bus.publish(ev.topic, ev.payload)
                sent_ids.append(ev.id)
            except Exception as exc:
                logger.exception("failed publish for outbox id %s: %s", ev.id, exc)
                failed_count += 1
                try:
                    self.repo.increment_attempts(ev.id)
                except Exception:
                    logger.exception("failed to increment attempts for %s", ev.id)

        if sent_ids:
            self.repo.mark_dispatched(sent_ids)

        # release locks for failed ones
        failed_ids = [e.id for e in events if e.id not in sent_ids]
        if failed_ids:
            self.repo.release_locks(failed_ids)

        return {"claimed": len(events), "sent": len(sent_ids), "failed": failed_count}


def main(bus: str | None = None):
    logging.basicConfig(level=logging.INFO)
    disp = SQLOutboxDispatcher(bus=bus)
    summary = disp.run_once()
    logger.info("SQL outbox dispatch summary: %s", summary)
    return summary


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--bus", help="bus type: local|rabbit|kafka", default=None)
    args = p.parse_args()
    main(args.bus)
