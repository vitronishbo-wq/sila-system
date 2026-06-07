"""
Tests for apps/backend/start_dlq_worker.py
Focus: DLQ consumer, alert handling, event recording
"""

import os
import pytest
from datetime import datetime
from unittest.mock import Mock, MagicMock, patch, call

# Import must happen after path setup
import sys
sys.path.insert(0, "/home/dev03wsl/sila-system/apps/backend")

from start_dlq_worker import DLQConsumer


class TestDLQConsumer:
    """Test DLQConsumer functionality"""

    def test_dlq_consumer_initialization(self):
        """Test DLQConsumer initialization"""
        with patch("start_dlq_worker.Connection"):
            consumer = DLQConsumer("amqp://guest:guest@localhost:5672/")

            assert consumer.broker_url == "amqp://guest:guest@localhost:5672/"
            assert consumer.dlx_exchange_name == "sila.automation.dlx"
            assert consumer.dlq_queue_name == "sila_dlq_main"
            assert consumer.dlq_stats["processed"] == 0
            assert consumer.dlq_stats["failed"] == 0
            assert consumer.dlq_stats["alerted"] == 0

    def test_dlq_consumer_stats_tracking(self):
        """Test statistics tracking"""
        with patch("start_dlq_worker.Connection"):
            consumer = DLQConsumer("amqp://localhost:5672/")

            consumer.dlq_stats["processed"] = 10
            consumer.dlq_stats["failed"] = 2
            consumer.dlq_stats["alerted"] = 1

            assert consumer.dlq_stats["processed"] == 10
            assert consumer.dlq_stats["failed"] == 2
            assert consumer.dlq_stats["alerted"] == 1

    def test_dlq_consumer_get_consumers(self):
        """Test get_consumers method"""
        with patch("start_dlq_worker.Connection"):
            consumer = DLQConsumer("amqp://localhost:5672/")

            mock_consumer_class = MagicMock()
            mock_channel = MagicMock()

            consumers = consumer.get_consumers(mock_consumer_class, mock_channel)

            assert len(consumers) == 1
            assert mock_consumer_class.called

    def test_dlq_consumer_handle_message_success(self):
        """Test successful DLQ message handling"""
        with patch("start_dlq_worker.Connection"):
            with patch.object(DLQConsumer, "_record_dlq_event") as mock_record:
                consumer = DLQConsumer("amqp://localhost:5672/")

                payload = {
                    "event_type": "transfer_failed",
                    "request": {"student_id": "TEST-001"},
                    "error": "Transfer validation failed",
                }

                consumer._handle_dlq_message(payload)

                # Verify recording was called
                mock_record.assert_called_once()
                call_args = mock_record.call_args
                assert call_args[0][0] == "transfer_failed"
                assert call_args[0][1] == "TEST-001"

    def test_dlq_consumer_handle_message_extraction(self):
        """Test student_id extraction from various payload formats"""
        with patch("start_dlq_worker.Connection"):
            with patch.object(DLQConsumer, "_record_dlq_event") as mock_record:
                consumer = DLQConsumer("amqp://localhost:5672/")

                # Format 1: student_id in request
                payload1 = {
                    "event_type": "transfer_failed",
                    "request": {"student_id": "STUDENT-001"},
                }
                consumer._handle_dlq_message(payload1)
                assert mock_record.call_args[0][1] == "STUDENT-001"

                # Format 2: student_id at root
                payload2 = {
                    "event_type": "transfer_failed",
                    "student_id": "STUDENT-002",
                }
                consumer._handle_dlq_message(payload2)
                assert mock_record.call_args[0][1] == "STUDENT-002"

    def test_dlq_consumer_record_event(self):
        """Test _record_dlq_event method"""
        with patch("start_dlq_worker.Connection"):
            consumer = DLQConsumer("amqp://localhost:5672/")

            payload = {
                "event_type": "transfer_failed",
                "request": {"student_id": "TEST-001"},
                "error": "Validation failed",
            }

            # Should not raise
            consumer._record_dlq_event(
                "transfer_failed",
                "TEST-001",
                "Validation failed",
                payload,
            )

    def test_dlq_consumer_send_alert_slack(self):
        """Test Slack alerting"""
        with patch("start_dlq_worker.Connection"):
            with patch.dict(os.environ, {"ALERT_WEBHOOK_URL": "https://hooks.slack.com/test"}):
                with patch("start_dlq_worker.requests.post") as mock_post:
                    mock_post.return_value.status_code = 200

                    consumer = DLQConsumer("amqp://localhost:5672/")
                    consumer._send_alert(
                        "transfer_failed",
                        "TEST-001",
                        "Validation error",
                        {"error": "detail"},
                    )

                    # Verify post was called
                    mock_post.assert_called_once()
                    call_args = mock_post.call_args
                    assert "https://hooks.slack.com/test" in call_args[0]

    def test_dlq_consumer_slack_alert_format(self):
        """Test Slack message format"""
        with patch("start_dlq_worker.Connection"):
            with patch.dict(os.environ, {"ALERT_WEBHOOK_URL": "https://hooks.slack.com/test"}):
                with patch("start_dlq_worker.requests.post") as mock_post:
                    mock_post.return_value.status_code = 200

                    consumer = DLQConsumer("amqp://localhost:5672/")
                    consumer._send_alert(
                        "transfer_failed",
                        "TEST-001",
                        "Validation error",
                        {"test": "payload"},
                    )

                    # Check payload format
                    call_kwargs = mock_post.call_args[1]
                    slack_payload = call_kwargs["json"]

                    assert "attachments" in slack_payload
                    assert slack_payload["attachments"][0]["color"] == "danger"
                    assert "TEST-001" in slack_payload["text"] or "TEST-001" in str(slack_payload)

    def test_dlq_consumer_print_stats(self):
        """Test statistics printing"""
        with patch("start_dlq_worker.Connection"):
            with patch("start_dlq_worker.logger") as mock_logger:
                consumer = DLQConsumer("amqp://localhost:5672/")
                consumer.dlq_stats["processed"] = 5
                consumer.dlq_stats["failed"] = 1
                consumer.dlq_stats["alerted"] = 1

                consumer.print_stats()

                # Verify logging was called
                mock_logger.info.assert_called()
                call_text = str(mock_logger.info.call_args)
                assert "processed=5" in call_text
                assert "failed=1" in call_text

    def test_dlq_consumer_dlq_callback_success(self):
        """Test _dlq_callback with successful processing"""
        with patch("start_dlq_worker.Connection"):
            with patch.object(DLQConsumer, "_handle_dlq_message"):
                consumer = DLQConsumer("amqp://localhost:5672/")
                mock_message = MagicMock()

                payload = {"event_type": "transfer_failed"}
                consumer._dlq_callback(payload, mock_message)

                # Verify message was acked
                mock_message.ack.assert_called_once()
                assert consumer.dlq_stats["processed"] == 1

    def test_dlq_consumer_dlq_callback_error(self):
        """Test _dlq_callback with error handling"""
        with patch("start_dlq_worker.Connection"):
            with patch.object(DLQConsumer, "_handle_dlq_message") as mock_handler:
                mock_handler.side_effect = Exception("Processing error")

                consumer = DLQConsumer("amqp://localhost:5672/")
                mock_message = MagicMock()

                payload = {"event_type": "transfer_failed"}
                consumer._dlq_callback(payload, mock_message)

                # Verify message was rejected
                mock_message.reject.assert_called_once()
                assert consumer.dlq_stats["failed"] == 1

    def test_dlq_consumer_on_connection_error(self):
        """Test connection error handling"""
        with patch("start_dlq_worker.Connection"):
            with patch("start_dlq_worker.logger") as mock_logger:
                consumer = DLQConsumer("amqp://localhost:5672/")
                consumer.on_connection_error(Exception("Connection lost"), 10)

                # Verify warning was logged
                mock_logger.warning.assert_called_once()

    def test_dlq_consumer_integration_env_vars(self):
        """Test DLQConsumer respects environment variables"""
        env_vars = {
            "RABBITMQ_URL": "amqp://user:pass@broker:5672/",
            "RABBITMQ_DLX_EXCHANGE": "custom.dlx",
            "RABBITMQ_DLQ_QUEUE": "custom_dlq",
        }

        with patch.dict(os.environ, env_vars):
            # Reload module to pick up env vars
            import importlib
            import start_dlq_worker

            importlib.reload(start_dlq_worker)

            with patch("start_dlq_worker.Connection"):
                consumer = start_dlq_worker.DLQConsumer(
                    os.getenv("RABBITMQ_URL", "amqp://localhost:5672/")
                )

                assert consumer.dlx_exchange_name == "custom.dlx"
                assert consumer.dlq_queue_name == "custom_dlq"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
