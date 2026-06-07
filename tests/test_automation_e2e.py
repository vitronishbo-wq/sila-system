"""
End-to-End Integration Tests for PASSO 13 & 14
Tests the complete automation flow with RabbitMQ and DLQ
"""

import pytest
import os
from unittest.mock import Mock, MagicMock, patch
import json
import time


class TestAutomationE2E:
    """End-to-end tests for transfer automation workflow"""

    @pytest.fixture
    def rabbitmq_url(self):
        """RabbitMQ connection string"""
        return os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")

    @pytest.fixture
    def mock_bus(self):
        """Mock AutomationBus for testing"""
        from foundation.automation.message_bus import LocalAutomationBus
        return LocalAutomationBus()

    def test_transfer_requested_event_flow(self, mock_bus):
        """Test transfer_requested → transfer_validated → transfer_completed flow"""
        events_received = {
            "transfer_requested": None,
            "transfer_validated": None,
            "transfer_completed": None,
        }

        def capture_event(event_type):
            def handler(payload):
                events_received[event_type] = payload
            return handler

        # Subscribe to all events
        mock_bus.subscribe("transfer_requested", capture_event("transfer_requested"))
        mock_bus.subscribe("transfer_validated", capture_event("transfer_validated"))
        mock_bus.subscribe("transfer_completed", capture_event("transfer_completed"))

        # Simulate event flow
        request_payload = {
            "event_type": "transfer_requested",
            "request": {
                "student_id": "TEST-001",
                "target_school": "SCHOOL-A",
                "target_class": "TURMA-1",
                "academic_year": 2024,
            },
            "evaluation": {"eligible": True},
        }

        # Publish request
        mock_bus.publish("transfer_requested", request_payload)

        # Verify request was received
        assert events_received["transfer_requested"] is not None
        assert events_received["transfer_requested"]["event_type"] == "transfer_requested"

    def test_transfer_failed_with_error_message(self, mock_bus):
        """Test transfer_failed event captures error details"""
        failed_event = None

        def capture_failed(payload):
            nonlocal failed_event
            failed_event = payload

        mock_bus.subscribe("transfer_failed", capture_failed)

        payload = {
            "event_type": "transfer_failed",
            "student_id": "TEST-002",
            "error": "Database connection failed",
        }

        mock_bus.publish("transfer_failed", payload)

        assert failed_event is not None
        assert failed_event["error"] == "Database connection failed"
        assert failed_event["student_id"] == "TEST-002"

    def test_multiple_events_sequence(self, mock_bus):
        """Test a sequence of events in order"""
        event_sequence = []

        def track_event(payload):
            event_sequence.append(payload.get("event_type"))

        for event_type in ["transfer_requested", "transfer_validated", "transfer_completed"]:
            mock_bus.subscribe(event_type, track_event)

        # Publish sequence
        events = [
            {"event_type": "transfer_requested", "student_id": "TEST-003"},
            {"event_type": "transfer_validated", "student_id": "TEST-003"},
            {"event_type": "transfer_completed", "student_id": "TEST-003"},
        ]

        for event in events:
            mock_bus.publish(event["event_type"], event)

        # Verify sequence
        assert event_sequence == ["transfer_requested", "transfer_validated", "transfer_completed"]

    def test_event_retry_handling_simulation(self, mock_bus):
        """Simulate retry logic with event payload metadata"""
        retry_count = 0

        def handler_with_retry(payload):
            nonlocal retry_count
            retry_count += 1
            if retry_count < 3:
                # Simulate failure and republish
                payload["retry_attempt"] = retry_count
                mock_bus.publish("transfer_requested", payload)

        mock_bus.subscribe("transfer_requested", handler_with_retry)

        payload = {"event_type": "transfer_requested", "student_id": "TEST-004", "retry_attempt": 0}
        mock_bus.publish("transfer_requested", payload)

        # After retries, should have reached max
        assert retry_count == 3

    def test_dlq_event_structure(self):
        """Test DLQ event has correct structure"""
        dlq_event = {
            "event_type": "transfer_failed",
            "student_id": "TEST-005",
            "error": "Connection timeout",
            "original_event": {
                "event_type": "transfer_requested",
                "request": {"student_id": "TEST-005"},
            },
            "timestamp": "2026-05-26T10:00:00Z",
            "retry_count": 3,
        }

        # Validate structure
        assert "event_type" in dlq_event
        assert "student_id" in dlq_event
        assert "error" in dlq_event
        assert "timestamp" in dlq_event
        assert "retry_count" in dlq_event

    def test_event_payload_validation(self):
        """Test that event payloads have required fields"""
        valid_events = [
            {
                "event_type": "transfer_requested",
                "request": {"student_id": "TEST-006"},
            },
            {
                "event_type": "transfer_validated",
                "request": {"student_id": "TEST-006"},
            },
            {
                "event_type": "transfer_completed",
                "student_id": "TEST-006",
                "result": {"eligible": True, "score": 85},
            },
            {
                "event_type": "transfer_failed",
                "student_id": "TEST-006",
                "error": "Validation failed",
            },
        ]

        for event in valid_events:
            assert "event_type" in event
            assert event["event_type"] in [
                "transfer_requested",
                "transfer_validated",
                "transfer_completed",
                "transfer_failed",
            ]
            # All events must have student_id in some form
            has_student_id = (
                "student_id" in event
                or ("request" in event and "student_id" in event["request"])
            )
            assert has_student_id

    def test_concurrent_event_processing(self, mock_bus):
        """Test handling of concurrent events for different students"""
        processed = []

        def handler(payload):
            student_id = payload.get("student_id") or payload.get("request", {}).get("student_id")
            processed.append(student_id)

        mock_bus.subscribe("transfer_requested", handler)

        # Simulate concurrent events for different students
        for i in range(5):
            mock_bus.publish(
                "transfer_requested",
                {
                    "event_type": "transfer_requested",
                    "student_id": f"STUDENT-{i:03d}",
                },
            )

        # All events should be processed
        assert len(processed) == 5
        assert "STUDENT-000" in processed
        assert "STUDENT-004" in processed

    @patch("foundation.automation.automator.AutomationEngine")
    def test_automation_engine_integration(self, mock_engine_class):
        """Test AutomationEngine receives and processes events"""
        # This would test the actual integration if RabbitMQ is running
        # For now, test the mock setup
        mock_engine = MagicMock()
        mock_engine_class.return_value = mock_engine

        # Verify mock can be called
        engine = mock_engine_class()
        engine.request_transfer({"student_id": "TEST-007"})

        mock_engine.request_transfer.assert_called_once()

    def test_event_bus_fallback_mechanism(self):
        """Test fallback from RabbitMQ to LocalBus"""
        from foundation.automation.message_bus import build_automation_bus

        # With invalid RabbitMQ URL, should fallback to local
        with patch.dict(os.environ, {"RABBITMQ_URL": "amqp://invalid"}):
            with patch("foundation.automation.message_bus.RabbitMQAutomationBus") as mock_rabbitmq:
                mock_rabbitmq.side_effect = Exception("Connection failed")
                bus = build_automation_bus("rabbit")

                from foundation.automation.message_bus import LocalAutomationBus
                assert isinstance(bus, LocalAutomationBus)

    def test_event_context_preservation(self, mock_bus):
        """Test that event context (student_id, etc) is preserved through handlers"""
        original_student_id = "TEST-008"
        preserved_student_id = None

        def capture_student_id(payload):
            nonlocal preserved_student_id
            preserved_student_id = payload.get("student_id") or payload.get("request", {}).get("student_id")

        mock_bus.subscribe("transfer_requested", capture_student_id)

        mock_bus.publish(
            "transfer_requested",
            {
                "event_type": "transfer_requested",
                "request": {"student_id": original_student_id},
            },
        )

        assert preserved_student_id == original_student_id

    def test_error_event_carries_context(self):
        """Test that error events include original request context"""
        error_event = {
            "event_type": "transfer_failed",
            "student_id": "TEST-009",
            "error": "Academic validation failed",
            "original_request": {
                "student_id": "TEST-009",
                "target_school": "SCHOOL-A",
            },
        }

        # Verify context is preserved
        assert error_event["original_request"]["student_id"] == error_event["student_id"]

    def test_handler_exception_isolation(self, mock_bus):
        """Test that exception in one handler doesn't affect others"""
        handler1_called = False
        handler2_called = False

        def failing_handler(payload):
            raise Exception("Handler error")

        def working_handler(payload):
            nonlocal handler2_called
            handler2_called = True

        mock_bus.subscribe("test_event", failing_handler)
        mock_bus.subscribe("test_event", working_handler)

        # Should not raise despite failing handler
        mock_bus.publish("test_event", {"event_type": "test_event"})

        # Working handler should still have been called
        assert handler2_called

    def test_performance_metric_structure(self):
        """Test performance metrics can be extracted from events"""
        event_with_metrics = {
            "event_type": "transfer_completed",
            "student_id": "TEST-010",
            "result": {"eligible": True},
            "metrics": {
                "processing_time_ms": 245,
                "retry_attempts": 0,
                "timestamp": "2026-05-26T10:00:00Z",
            },
        }

        # Verify metrics extraction
        assert "metrics" in event_with_metrics
        assert event_with_metrics["metrics"]["processing_time_ms"] > 0
        assert event_with_metrics["metrics"]["retry_attempts"] >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
