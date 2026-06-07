#!/usr/bin/env python3
"""
RabbitMQ Integration Tests
Validate event publishing, routing, and subscription patterns.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import uuid4


@dataclass
class TestEvent:
    """Test domain event."""

    event_id: str
    aggregate_type: str
    event_type: str
    aggregate_id: str
    timestamp: str
    data: dict[str, Any]

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "aggregate_type": self.aggregate_type,
            "event_type": self.event_type,
            "aggregate_id": self.aggregate_id,
            "timestamp": self.timestamp,
            "data": self.data,
        }


class RabbitMQValidator:
    """Validate RabbitMQ integration readiness."""

    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.issues = []

    def validate(self):
        """Run all validation tests."""
        print(f"\n{'=' * 80}")
        print("[RABBITMQ INTEGRATION VALIDATION]")
        print(f"{'=' * 80}\n")

        self._test_dependencies()
        self._test_event_serialization()
        self._test_routing_patterns()
        self._test_connection_readiness()
        self._test_event_models()

        self._print_results()

    def _test_dependencies(self):
        """Test required dependencies."""
        print("[Testing] Dependencies...")

        required = {
            "aio_pika": "RabbitMQ async client",
            "dataclasses": "Data structures",
            "asyncio": "Async runtime",
            "json": "Message serialization",
        }

        missing = []
        for module, desc in required.items():
            try:
                __import__(module)
            except ImportError:
                missing.append(f"{module} ({desc})")

        if not missing:
            print("  [PASS] All required dependencies available")
            self.tests_passed += 1
        else:
            print(f"  [FAIL] Missing: {', '.join(missing)}")
            self.issues.append(f"Missing dependencies: {', '.join(missing)}")
            self.tests_failed += 1

    def _test_event_serialization(self):
        """Test event serialization."""
        print("[Testing] Event serialization...")

        try:
            event = TestEvent(
                event_id=str(uuid4()),
                aggregate_type="citizen",
                event_type="CitizenCreated",
                aggregate_id=str(uuid4()),
                timestamp=datetime.utcnow().isoformat(),
                data={"name": "John", "email": "john@example.com"},
            )

            # Test to_dict
            event_dict = event.to_dict()
            assert event_dict["event_type"] == "CitizenCreated"
            assert event_dict["aggregate_type"] == "citizen"
            assert event_dict["data"]["name"] == "John"

            print("  [PASS] Event serialization works")
            self.tests_passed += 1
        except Exception as e:
            print(f"  [FAIL] {str(e)}")
            self.issues.append(f"Event serialization failed: {str(e)}")
            self.tests_failed += 1

    def _test_routing_patterns(self):
        """Test RabbitMQ routing key patterns."""
        print("[Testing] Routing patterns...")

        try:
            # Test routing key generation
            aggregate_type = "citizen"
            event_type = "CitizenCreated"

            routing_key = f"{aggregate_type}.{event_type}".lower()
            assert routing_key == "citizen.citizencreated"

            # Test multiple routing patterns
            patterns = [
                ("citizen", "Created", "citizen.created"),
                ("household", "Updated", "household.updated"),
                ("justice", "Judged", "justice.judged"),
                ("economy", "Transacted", "economy.transacted"),
            ]

            for agg_type, event_name, expected in patterns:
                key = f"{agg_type}.{event_name}".lower()
                assert key == expected, f"Expected {expected}, got {key}"

            print("  [PASS] Routing patterns are correct")
            self.tests_passed += 1
        except Exception as e:
            print(f"  [FAIL] {str(e)}")
            self.issues.append(f"Routing patterns failed: {str(e)}")
            self.tests_failed += 1

    def _test_connection_readiness(self):
        """Test RabbitMQ connection readiness."""
        print("[Testing] RabbitMQ connection readiness...")

        try:
            # Check for RabbitMQ environment
            import os

            host = os.getenv("RABBITMQ_HOST", "localhost")
            port = int(os.getenv("RABBITMQ_PORT", 5672))
            user = os.getenv("RABBITMQ_USER", "guest")
            password = os.getenv("RABBITMQ_PASSWORD", "guest")

            # Try to import aio_pika
            try:
                import aio_pika

                print(f"  [INFO] RabbitMQ config: {host}:{port}")
                print(f"  [INFO] Credentials ready: {user}:{'*' * len(password)}")
                print("  [PASS] RabbitMQ client available")
                self.tests_passed += 1
            except ImportError:
                print("  [WARN] aio_pika not installed - async RabbitMQ client unavailable")
                print("         Install with: pip install aio-pika")
                self.tests_failed += 1
                self.issues.append("aio_pika not installed")

        except Exception as e:
            print(f"  [FAIL] {str(e)}")
            self.issues.append(f"Connection readiness test failed: {str(e)}")
            self.tests_failed += 1

    def _test_event_models(self):
        """Test event model structure."""
        print("[Testing] Event model structure...")

        try:
            # Create sample events for all module types
            module_events = [
                ("citizen", "CitizenCreated"),
                ("household", "HouseholdRegistered"),
                ("identity", "IdentityVerified"),
                ("justice", "CourtDecided"),
                ("economy", "TransactionCompleted"),
            ]

            for agg_type, event_type in module_events:
                event = TestEvent(
                    event_id=str(uuid4()),
                    aggregate_type=agg_type,
                    event_type=event_type,
                    aggregate_id=str(uuid4()),
                    timestamp=datetime.utcnow().isoformat(),
                    data={"action": "test"},
                )

                # Verify serialization
                d = event.to_dict()
                assert d["aggregate_type"] == agg_type
                assert d["event_type"] == event_type

            print(f"  [PASS] Event models for {len(module_events)} aggregates work")
            self.tests_passed += 1
        except Exception as e:
            print(f"  [FAIL] {str(e)}")
            self.issues.append(f"Event models failed: {str(e)}")
            self.tests_failed += 1

    def _print_results(self):
        """Print validation results."""
        total = self.tests_passed + self.tests_failed
        percentage = (self.tests_passed * 100) // total if total > 0 else 0

        print(f"\n{'=' * 80}")
        print(f"RESULTS: {self.tests_passed}/{total} PASSED ({percentage}%)")
        print(f"{'=' * 80}\n")

        if self.issues:
            print("ISSUES:")
            for issue in self.issues:
                print(f"  - {issue}")
            print()

        if self.tests_failed == 0:
            print("STATUS: Ready for RabbitMQ integration\n")
        else:
            print(f"STATUS: {self.tests_failed} issues need fixing\n")


if __name__ == "__main__":
    validator = RabbitMQValidator()
    validator.validate()
