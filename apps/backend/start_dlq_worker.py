#!/usr/bin/env python3
"""
Dead Letter Queue (DLQ) Worker

Processes messages that have failed processing in the main automation queues.
This worker:
- Consumes from the DLQ (sila_dlq_main)
- Logs critical failures with full context
- Sends alerts (Slack, PagerDuty, etc.)
- Enables manual intervention for failed transfers
"""

import logging
import os
import signal
import time
from datetime import datetime
from typing import Any

from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin

logger = logging.getLogger(__name__)

# Configuration from environment
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672//")
DLQ_QUEUE_NAME = os.getenv("RABBITMQ_DLQ_QUEUE", "sila_dlq_main")
DLX_EXCHANGE_NAME = os.getenv("RABBITMQ_DLX_EXCHANGE", "sila.automation.dlx")
ALERT_WEBHOOK_URL = os.getenv("ALERT_WEBHOOK_URL")  # Optional Slack webhook
ALERT_EMAIL = os.getenv("ALERT_EMAIL")  # Optional email alerts


class DLQConsumer(ConsumerMixin):
    """Consumer for Dead Letter Queue messages."""

    def __init__(self, broker_url: str) -> None:
        self.connection = Connection(broker_url)
        self.broker_url = broker_url

        # Create DLX exchange and DLQ queue
        self.dlx_exchange = Exchange(DLX_EXCHANGE_NAME, type="topic", durable=True)
        self.dlq_queue = Queue(
            DLQ_QUEUE_NAME,
            exchange=self.dlx_exchange,
            routing_key="dlq.#",
            durable=True,
        )

        self.dlq_stats = {
            "processed": 0,
            "failed": 0,
            "alerted": 0,
            "start_time": datetime.utcnow(),
        }

    def get_consumers(self, Consumer, channel):
        """Return consumer for DLQ queue."""
        return [Consumer(queue=self.dlq_queue, callbacks=[self._dlq_callback], accept=["json"])]

    def _dlq_callback(self, body: dict[str, Any], message) -> None:
        """Process a DLQ message."""
        try:
            self._handle_dlq_message(body)
            message.ack()
            self.dlq_stats["processed"] += 1
        except Exception:
            logger.exception("DLQ callback failed for message: %s", body)
            self.dlq_stats["failed"] += 1
            message.reject()

    def _handle_dlq_message(self, payload: dict[str, Any]) -> None:
        """Process a message that ended up in DLQ."""
        event_type = payload.get("event_type", "unknown")
        student_id = payload.get("request", {}).get("student_id", payload.get("student_id", "N/A"))
        error_msg = payload.get("error", "No error message provided")

        # Log critical failure
        logger.critical(
            "DLQ_ALERT: event=%s student_id=%s error=%s payload=%s",
            event_type,
            student_id,
            error_msg,
            payload,
        )

        # Record to database for manual review (if applicable)
        self._record_dlq_event(event_type, student_id, error_msg, payload)

        # Send alert if configured
        if ALERT_WEBHOOK_URL or ALERT_EMAIL:
            self._send_alert(event_type, student_id, error_msg, payload)

    def _record_dlq_event(self, event_type: str, student_id: str, error: str, payload: dict[str, Any]) -> None:
        """Record DLQ event to database/logs for audit trail."""
        # This is a placeholder for database recording
        # In production, you would:
        # 1. Connect to PostgreSQL
        # 2. Insert into dlq_events table
        # 3. Include timestamp, event_type, student_id, error, payload
        #
        # Example SQL:
        # INSERT INTO dlq_events (event_type, student_id, error, payload, created_at)
        # VALUES (%s, %s, %s, %s, now())

        logger.info(
            "DLQ_EVENT_RECORDED: event=%s student_id=%s error=%s timestamp=%s",
            event_type,
            student_id,
            error,
            datetime.utcnow().isoformat(),
        )

    def _send_alert(self, event_type: str, student_id: str, error: str, payload: dict[str, Any]) -> None:
        """Send alert via Slack, email, or other channels."""
        alert_msg = (
            f"🚨 **Dead Letter Queue Alert**\n"
            f"Event: {event_type}\n"
            f"Student ID: {student_id}\n"
            f"Error: {error}\n"
            f"Timestamp: {datetime.utcnow().isoformat()}\n"
        )

        # Alert via Slack if webhook configured
        if ALERT_WEBHOOK_URL:
            self._send_slack_alert(alert_msg, payload)

        # Alert via email if configured
        if ALERT_EMAIL:
            logger.warning("Email alerting not yet implemented. Would send to: %s", ALERT_EMAIL)

        self.dlq_stats["alerted"] += 1

    def _send_slack_alert(self, message: str, payload: dict[str, Any]) -> None:
        """Send alert to Slack."""
        try:
            import requests

            slack_payload = {
                "text": message,
                "attachments": [
                    {
                        "color": "danger",
                        "title": "Full Payload",
                        "text": str(payload)[:1000],  # Truncate if too long
                        "footer": "SILA System DLQ",
                        "ts": int(time.time()),
                    }
                ],
            }

            response = requests.post(ALERT_WEBHOOK_URL, json=slack_payload, timeout=5)
            if response.status_code == 200:
                logger.info("Slack alert sent successfully")
            else:
                logger.warning("Slack alert failed with status %d: %s", response.status_code, response.text)
        except ImportError:
            logger.warning("requests library not available for Slack alert")
        except Exception:
            logger.exception("Failed to send Slack alert")

    def print_stats(self) -> None:
        """Print DLQ consumer statistics."""
        uptime = (datetime.utcnow() - self.dlq_stats["start_time"]).total_seconds()
        stats_msg = (
            f"DLQ Consumer Stats: "
            f"processed={self.dlq_stats['processed']} "
            f"failed={self.dlq_stats['failed']} "
            f"alerted={self.dlq_stats['alerted']} "
            f"uptime_seconds={uptime:.1f}"
        )
        logger.info(stats_msg)

    def on_connection_error(self, exc, interval):
        logger.warning("DLQ consumer connection error: %s, retrying in %s seconds", exc, interval)


def main() -> None:
    """Main entry point for DLQ worker."""
    logging.basicConfig(
        level=logging.INFO,
        format="[dlq-worker] %(asctime)s %(name)s %(levelname)s %(message)s",
    )

    logger.info("Initializing DLQ Worker")
    logger.info("Configuration: RABBITMQ_URL=%s DLQ_QUEUE=%s", RABBITMQ_URL, DLQ_QUEUE_NAME)

    if ALERT_WEBHOOK_URL:
        logger.info("Slack alerts enabled: %s", ALERT_WEBHOOK_URL)
    if ALERT_EMAIL:
        logger.info("Email alerts enabled: %s", ALERT_EMAIL)

    consumer = DLQConsumer(RABBITMQ_URL)
    stopped = False

    def shutdown(signum, frame):
        nonlocal stopped
        logger.info("Shutdown requested (signal %s)", signum)
        stopped = True

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    logger.info("DLQ Worker started and listening on queue=%s", DLQ_QUEUE_NAME)

    stats_interval = 300  # Print stats every 5 minutes
    last_stats = time.time()

    try:
        while not stopped:
            current_time = time.time()
            if current_time - last_stats >= stats_interval:
                consumer.print_stats()
                last_stats = current_time

            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received")
    finally:
        logger.info("Stopping DLQ worker")
        consumer.print_stats()
        try:
            # Graceful shutdown
            consumer.should_stop = True
        except Exception:
            logger.exception("Error during graceful shutdown")


if __name__ == "__main__":
    main()
