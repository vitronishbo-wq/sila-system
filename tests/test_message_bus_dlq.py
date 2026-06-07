"""
Tests for foundation/automation/message_bus.py
Focus: DLX/DLQ configuration and message routing
"""

import os
import pytest
from unittest.mock import Mock, MagicMock, patch

from foundation.automation.message_bus import (
    LocalAutomationBus,
    RabbitMQAutomationBus,
    build_automation_bus,
)


class TestLocalAutomationBus:
    """Test LocalAutomationBus (in-memory fallback)"""

    def test_local_bus_publish_and_subscribe(self):
        """Test basic publish/subscribe in local bus"""
        bus = LocalAutomationBus()
        received = []

        def handler(event):
            received.append(event)

        # Subscribe and publish
        bus.subscribe("test_event", handler)
        bus.publish("test_event", {"data": "test"})

        # Verify
        assert len(received) == 1
        assert received[0]["data"] == "test"

    def test_local_bus_start_stop(self):
        """Test start/stop methods (no-op for local bus)"""
        bus = LocalAutomationBus()
        bus.start()  # Should not raise
        bus.stop()   # Should not raise

    def test_local_bus_multiple_handlers(self):
        """Test multiple handlers for same event"""
        bus = LocalAutomationBus()
        handler1_calls = []
        handler2_calls = []

        def handler1(event):
            handler1_calls.append(event)

        def handler2(event):
            handler2_calls.append(event)

        bus.subscribe("event", handler1)
        bus.subscribe("event", handler2)
        bus.publish("event", {"data": "test"})

        assert len(handler1_calls) == 1
        assert len(handler2_calls) == 1


class TestRabbitMQAutomationBus:
    """Test RabbitMQAutomationBus with DLX/DLQ support"""

    def test_rabbitmq_bus_initialization(self):
        """Test RabbitMQAutomationBus initialization"""
        with patch("foundation.automation.message_bus.Connection"):
            bus = RabbitMQAutomationBus(
                broker_url="amqp://guest:guest@localhost:5672/",
                dlx_enabled=True,
                max_retries=3,
            )

            assert bus.exchange_name == "sila.automation"
            assert bus.dlx_exchange_name == "sila.automation.dlx"
            assert bus.dlq_queue_name == "sila_dlq_main"
            assert bus.dlx_enabled is True
            assert bus.max_retries == 3

    def test_rabbitmq_bus_auto_detect_from_env(self):
        """Test auto-detection of RABBITMQ_URL from environment"""
        with patch.dict(os.environ, {"RABBITMQ_URL": "amqp://custom:custom@broker:5672/"}):
            with patch("foundation.automation.message_bus.Connection"):
                bus = RabbitMQAutomationBus()
                assert bus.broker_url == "amqp://custom:custom@broker:5672/"

    def test_rabbitmq_bus_dlx_setup_disabled(self):
        """Test initialization with DLX disabled"""
        with patch("foundation.automation.message_bus.Connection"):
            bus = RabbitMQAutomationBus(dlx_enabled=False)
            assert bus.dlx_enabled is False
            assert bus.dlx_exchange is None

    def test_setup_dlx_for_queue(self):
        """Test DLX configuration for a queue"""
        from kombu import Queue, Exchange

        with patch("foundation.automation.message_bus.Connection"):
            bus = RabbitMQAutomationBus(dlx_enabled=True)
            exchange = Exchange("test.exchange", type="topic", durable=True)
            queue = Queue("test_queue", exchange=exchange, routing_key="test_key", durable=True)

            # Apply DLX setup
            configured_queue = bus._setup_dlx_for_queue(queue)

            # Verify DLX arguments added
            assert configured_queue.queue_arguments is not None
            assert "x-dead-letter-exchange" in configured_queue.queue_arguments
            assert configured_queue.queue_arguments["x-dead-letter-exchange"] == "sila.automation.dlx"
            assert "x-dead-letter-routing-key" in configured_queue.queue_arguments
            assert configured_queue.queue_arguments["x-dead-letter-routing-key"] == "dlq.test_key"

    def test_rabbitmq_bus_subscribe_creates_queue(self):
        """Test that subscribe() creates a queue with DLX"""
        with patch("foundation.automation.message_bus.Connection"):
            bus = RabbitMQAutomationBus(dlx_enabled=True)

            def handler(event):
                pass

            bus.subscribe("transfer_requested", handler)

            # Verify queue was created
            assert "transfer_requested" in bus._queues
            queue = bus._queues["transfer_requested"]
            assert queue.name == "sila_transfer_requested"
            assert queue.routing_key == "transfer_requested"

    def test_rabbitmq_bus_publish_integration(self):
        """Test publish method with mocked Connection"""
        with patch("foundation.automation.message_bus.Connection") as mock_conn:
            with patch("foundation.automation.message_bus.Producer") as mock_producer:
                bus = RabbitMQAutomationBus()

                event = {
                    "event_type": "transfer_requested",
                    "request": {"student_id": "TEST-001"},
                }
                bus.publish("transfer_requested", event)

                # Verify Connection and Producer were called
                mock_conn.assert_called_once()
                mock_producer.assert_called_once()

                # Verify publish was called on producer instance
                producer_instance = mock_producer.return_value
                assert producer_instance.publish.called

    def test_build_automation_bus_rabbitmq(self):
        """Test build_automation_bus() with RabbitMQ"""
        with patch.dict(os.environ, {"RABBITMQ_URL": "amqp://guest:guest@localhost:5672/"}):
            with patch("foundation.automation.message_bus.RabbitMQAutomationBus") as mock_rabbitmq:
                mock_rabbitmq.return_value = MagicMock()
                bus = build_automation_bus("rabbit")
                mock_rabbitmq.assert_called_once()

    def test_build_automation_bus_local(self):
        """Test build_automation_bus() with local bus"""
        bus = build_automation_bus("local")
        assert isinstance(bus, LocalAutomationBus)

    def test_build_automation_bus_auto_detect_rabbitmq(self):
        """Test build_automation_bus() auto-detects RabbitMQ from env"""
        with patch.dict(os.environ, {"RABBITMQ_URL": "amqp://guest:guest@localhost:5672/"}):
            with patch("foundation.automation.message_bus.RabbitMQAutomationBus") as mock_rabbitmq:
                mock_rabbitmq.return_value = MagicMock()
                bus = build_automation_bus()  # No explicit type
                mock_rabbitmq.assert_called_once()

    def test_build_automation_bus_fallback_on_error(self):
        """Test build_automation_bus() falls back to local on RabbitMQ error"""
        with patch.dict(os.environ, {"RABBITMQ_URL": "amqp://invalid"}):
            with patch("foundation.automation.message_bus.RabbitMQAutomationBus") as mock_rabbitmq:
                mock_rabbitmq.side_effect = Exception("Connection failed")
                bus = build_automation_bus("rabbit")
                assert isinstance(bus, LocalAutomationBus)

    def test_rabbitmq_bus_env_config_dlq_max_retries(self):
        """Test DLQ_MAX_RETRIES environment variable"""
        with patch.dict(os.environ, {"DLQ_MAX_RETRIES": "5"}):
            with patch("foundation.automation.message_bus.Connection"):
                bus = RabbitMQAutomationBus()
                assert bus.max_retries == 5

    def test_rabbitmq_bus_env_config_dlq_disabled(self):
        """Test DLQ_ENABLED environment variable"""
        with patch.dict(os.environ, {"DLQ_ENABLED": "false"}):
            with patch("foundation.automation.message_bus.Connection"):
                bus = RabbitMQAutomationBus()
                assert bus.dlx_enabled is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
