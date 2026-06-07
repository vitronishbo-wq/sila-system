from __future__ import annotations

import json
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


class LocalEventBus:
    def publish(self, topic: str, event: dict[str, Any]) -> None:
        logger.info("LocalEventBus publish: %s %s", topic, event)


class OutboxDispatcher:
    def __init__(self, outbox_path: str | None = None, sent_path: str | None = None, bus=None) -> None:
        self.outbox_path = outbox_path or os.getenv("OUTBOX_PATH", "data/foundation_outbox.jsonl")
        self.sent_path = sent_path or (self.outbox_path + ".sent")
        os.makedirs(os.path.dirname(self.outbox_path), exist_ok=True)
        self.bus = bus or LocalEventBus()

    def dispatch_once(self) -> dict[str, int]:
        """Process the outbox file once: attempt to publish each event.

        On success a record is appended to `sent_path`. Failed events are
        kept in the outbox file for retry.
        Returns summary counts.
        """
        if not os.path.exists(self.outbox_path):
            return {"read": 0, "sent": 0, "failed": 0}

        remaining: list[str] = []
        sent_count = 0
        read_count = 0

        with open(self.outbox_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                read_count += 1
                try:
                    rec = json.loads(line)
                    topic = rec.get("topic")
                    event = rec.get("event")
                    if not topic or event is None:
                        raise ValueError("malformed outbox record")
                    self.bus.publish(topic, event)
                    with open(self.sent_path, "a", encoding="utf-8") as sf:
                        sf.write(line + "\n")
                    sent_count += 1
                except Exception as exc:
                    logger.exception("failed to publish outbox record: %s", exc)
                    remaining.append(line)

        # overwrite outbox with remaining (failed) records
        with open(self.outbox_path, "w", encoding="utf-8") as f:
            for l in remaining:
                f.write(l + "\n")

        return {"read": read_count, "sent": sent_count, "failed": len(remaining)}


def _build_bus(bus_type: str):
    bus_type = (bus_type or "").lower()
    if bus_type in ("rabbit", "rabbitmq"):
        try:
            from .adapters.rabbitmq import RabbitMQEventBus

            return RabbitMQEventBus()
        except Exception as exc:
            raise RuntimeError("RabbitMQ adapter unavailable: %s" % exc)
    if bus_type in ("kafka",):
        try:
            from .adapters.kafka import KafkaEventBus

            return KafkaEventBus()
        except Exception as exc:
            raise RuntimeError("Kafka adapter unavailable: %s" % exc)
    return LocalEventBus()


def main_one_shot(bus_type: str | None = None) -> dict[str, int]:
    bus_type = bus_type or os.getenv("OUTBOX_BUS", "local")
    bus = _build_bus(bus_type)
    dispatcher = OutboxDispatcher(bus=bus)
    summary = dispatcher.dispatch_once()
    logger.info("Outbox dispatch summary: %s", summary)
    return summary


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO)
    p = argparse.ArgumentParser()
    p.add_argument("--bus", help="bus type: local|rabbit|kafka", default=None)
    args = p.parse_args()
    main_one_shot(args.bus)
