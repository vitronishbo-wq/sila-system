"""
Integration Tests for CQRS Command → Event → Handler flows.
Tests end-to-end domain event sourcing and compliance.

Pytest fixtures and base test utilities are in conftest.py
"""

from datetime import date
from uuid import uuid4

import pytest

from apps.backend.app.core.events.domain_event import DomainEvent
from apps.backend.app.core.events.event_bus import InMemoryEventBus
from apps.backend.app.infrastructure.event_sourcing.event_store import InMemoryEventStore


@pytest.mark.asyncio
class TestEventSourcing:
    """Test event store persistence and replay."""

    @pytest.fixture
    def event_store(self) -> InMemoryEventStore:
        """Provide an event store instance (not async)."""
        return InMemoryEventStore()

    async def test_append_single_event(self, event_store: InMemoryEventStore):
        """Test appending a single event to the store."""
        from apps.backend.app.modules.justice.domain.events import CitizenCreated

        event = CitizenCreated(
            aggregate_id=uuid4(),
            aggregate_type="Citizen",
            event_type="CitizenCreated",
            first_name="João",
            last_name="Silva",
            birth_date=date(1990, 1, 15),
            birth_place="Lisbon",
            nationality="PT",
        )

        await event_store.append(event)
        events = await event_store.get_all_events()

        assert len(events) == 1
        assert events[0].aggregate_id == event.aggregate_id
        assert events[0].first_name == "João"

    async def test_append_batch_events(self, event_store: InMemoryEventStore):
        """Test appending multiple events atomically."""
        from apps.backend.app.modules.justice.domain.events import (
            CitizenCreated,
            CitizenIdentityDocumentIssued,
        )

        citizen_id = uuid4()

        events = [
            CitizenCreated(
                aggregate_id=citizen_id,
                aggregate_type="Citizen",
                event_type="CitizenCreated",
                first_name="Maria",
                last_name="Santos",
                birth_date=date(1985, 5, 20),
                birth_place="Porto",
                nationality="PT",
            ),
            CitizenIdentityDocumentIssued(
                aggregate_id=citizen_id,
                aggregate_type="Citizen",
                event_type="CitizenIdentityDocumentIssued",
                document_number="12345678",
                document_type="ID_CARD",
                issue_date=date(2023, 1, 1),
                issuing_authority="IRN",
            ),
        ]

        await event_store.append_batch(events)
        stored_events = await event_store.get_all_events()

        assert len(stored_events) == 2
        assert stored_events[0].event_type == "CitizenCreated"
        assert stored_events[1].event_type == "CitizenIdentityDocumentIssued"

    async def test_get_events_for_aggregate(self, event_store: InMemoryEventStore):
        """Test retrieving all events for a specific aggregate."""
        from apps.backend.app.modules.justice.domain.events import CitizenCreated

        citizen_id_1 = uuid4()
        citizen_id_2 = uuid4()

        # Create events for two different citizens
        await event_store.append(
            CitizenCreated(
                aggregate_id=citizen_id_1,
                aggregate_type="Citizen",
                event_type="CitizenCreated",
                first_name="Alice",
                last_name="Johnson",
                birth_date=date(1990, 1, 1),
                birth_place="Lisbon",
                nationality="PT",
            )
        )

        await event_store.append(
            CitizenCreated(
                aggregate_id=citizen_id_2,
                aggregate_type="Citizen",
                event_type="CitizenCreated",
                first_name="Bob",
                last_name="Smith",
                birth_date=date(1995, 2, 2),
                birth_place="Porto",
                nationality="PT",
            )
        )

        # Retrieve events for first citizen only
        events = await event_store.get_events_for_aggregate(citizen_id_1)

        assert len(events) == 1
        assert events[0].aggregate_id == citizen_id_1
        assert events[0].first_name == "Alice"

    async def test_get_events_by_type(self, event_store: InMemoryEventStore):
        """Test retrieving events by type (for compliance audits)."""
        from apps.backend.app.modules.justice.domain.events import (
            BirthRecordCreated,
            CitizenCreated,
            CitizenIdentityDocumentIssued,
        )

        citizen_id = uuid4()
        birth_record_id = uuid4()

        await event_store.append(
            CitizenCreated(
                aggregate_id=citizen_id,
                aggregate_type="Citizen",
                event_type="CitizenCreated",
                first_name="Test",
                last_name="User",
                birth_date=date(2000, 1, 1),
                birth_place="Lisbon",
                nationality="PT",
            )
        )

        await event_store.append(
            CitizenIdentityDocumentIssued(
                aggregate_id=citizen_id,
                aggregate_type="Citizen",
                event_type="CitizenIdentityDocumentIssued",
                document_number="ID-001",
                document_type="ID_CARD",
                issue_date=date(2023, 1, 1),
                issuing_authority="IRN",
            )
        )

        await event_store.append(
            BirthRecordCreated(
                aggregate_id=birth_record_id,
                aggregate_type="BirthRecord",
                event_type="BirthRecordCreated",
                child_name="Child",
                birth_date=date(2010, 6, 15),
                birth_place="Lisbon",
                registering_authority="IRN",
            )
        )

        # Query for all document issuance events
        compliance_events = await event_store.get_events_by_type("CitizenIdentityDocumentIssued")

        assert len(compliance_events) == 1
        assert compliance_events[0].document_number == "ID-001"


@pytest.mark.asyncio
class TestEventBus:
    """Test event bus publishing and subscription."""

    @pytest.fixture
    def event_bus(self) -> InMemoryEventBus:
        """Provide an event bus instance (not async)."""
        return InMemoryEventBus()

    async def test_publish_and_subscribe(self, event_bus: InMemoryEventBus):
        """Test publishing and subscribing to events."""
        from apps.backend.app.modules.justice.domain.events import CitizenCreated

        received_events = []

        async def handler(event: DomainEvent):
            received_events.append(event)

        # Subscribe to event
        await event_bus.subscribe("CitizenCreated", handler)

        # Publish event
        event = CitizenCreated(
            aggregate_id=uuid4(),
            aggregate_type="Citizen",
            event_type="CitizenCreated",
            first_name="Carlos",
            last_name="Oliveira",
            birth_date=date(2000, 1, 1),
            birth_place="Covilhã",
            nationality="PT",
        )

        await event_bus.publish(event)

        # Verify handler was called
        assert len(received_events) == 1
        assert received_events[0].aggregate_id == event.aggregate_id

    async def test_unsubscribe(self, event_bus: InMemoryEventBus):
        """Test unsubscribing from events."""
        from apps.backend.app.modules.justice.domain.events import CitizenCreated

        received_events = []

        async def handler(event: DomainEvent):
            received_events.append(event)

        # Subscribe and unsubscribe
        await event_bus.subscribe("CitizenCreated", handler)
        await event_bus.unsubscribe("CitizenCreated", handler)

        # Publish event
        event = CitizenCreated(
            aggregate_id=uuid4(),
            aggregate_type="Citizen",
            event_type="CitizenCreated",
            first_name="Diana",
            last_name="Costa",
            birth_date=date(2001, 3, 3),
            birth_place="Aveiro",
            nationality="PT",
        )

        await event_bus.publish(event)

        # Handler should NOT be called
        assert len(received_events) == 0

    async def test_publish_batch(self, event_bus: InMemoryEventBus):
        """Test publishing multiple events."""
        from apps.backend.app.modules.justice.domain.events import CitizenCreated

        received_events = []

        async def handler(event: DomainEvent):
            received_events.append(event)

        await event_bus.subscribe("CitizenCreated", handler)

        # Create and publish batch
        events = [
            CitizenCreated(
                aggregate_id=uuid4(),
                aggregate_type="Citizen",
                event_type="CitizenCreated",
                first_name=f"Person{i}",
                last_name="Batch",
                birth_date=date(2000 + i, 1, 1),
                birth_place="Lisbon",
                nationality="PT",
            )
            for i in range(3)
        ]

        await event_bus.publish_batch(events)

        # All events should be received
        assert len(received_events) == 3


@pytest.mark.asyncio
class TestCQRSCommandToEvent:
    """Test CQRS pattern: Command → Event → Handler."""

    async def test_citizen_registration_flow(self):
        """Test complete CQRS flow for citizen registration."""
        from apps.backend.app.modules.justice.application.commands import (
            RegisterCitizenCommandHandler,
        )
        from apps.backend.app.modules.justice.domain.events import CitizenCreated

        # Setup
        event_bus = InMemoryEventBus()
        event_store = InMemoryEventStore()
        handler = RegisterCitizenCommandHandler(event_bus)

        # Track events
        captured_events = []

        async def capture_event(event: DomainEvent):
            captured_events.append(event)
            await event_store.append(event)

        await event_bus.subscribe("CitizenCreated", capture_event)

        # Execute command
        citizen_id = uuid4()
        correlation_id = uuid4()
        user_id = uuid4()

        await handler.handle(
            citizen_id=citizen_id,
            first_name="Fernando",
            last_name="Mendes",
            birth_date=date(1980, 6, 30),
            birth_place="Évora",
            nationality="PT",
            correlation_id=correlation_id,
            user_id=user_id,
        )

        # Verify event was published
        assert len(captured_events) == 1
        assert isinstance(captured_events[0], CitizenCreated)
        assert captured_events[0].first_name == "Fernando"
        assert captured_events[0].correlation_id == correlation_id

        # Verify event was persisted
        stored_events = await event_store.get_events_for_aggregate(citizen_id)
        assert len(stored_events) == 1

    async def test_identity_document_issuance_flow(self):
        """Test CQRS flow for identity document issuance (ACAO compliance)."""
        from apps.backend.app.modules.justice.application.commands import (
            IssueIdentityDocumentCommandHandler,
        )
        from apps.backend.app.modules.justice.domain.events import CitizenIdentityDocumentIssued

        # Setup
        event_bus = InMemoryEventBus()
        event_store = InMemoryEventStore()
        handler = IssueIdentityDocumentCommandHandler(event_bus)

        captured_events = []

        async def capture_event(event: DomainEvent):
            captured_events.append(event)
            await event_store.append(event)

        await event_bus.subscribe("CitizenIdentityDocumentIssued", capture_event)

        # Execute command
        citizen_id = uuid4()

        await handler.handle(
            citizen_id=citizen_id,
            document_number="PT12345678",
            document_type="BILHETE_IDENTIDADE",
            issue_date=date(2023, 3, 15),
            expiry_date=date(2033, 3, 15),
            issuing_authority="IRN",
            correlation_id=uuid4(),
            user_id=uuid4(),
        )

        # Verify ACAO compliance event was published
        assert len(captured_events) == 1
        assert isinstance(captured_events[0], CitizenIdentityDocumentIssued)
        assert captured_events[0].document_number == "PT12345678"

        # Verify compliance metadata
        assert "compliance_requirement" in captured_events[0].metadata


@pytest.mark.asyncio
class TestEventSerialization:
    """Test event serialization for storage and transmission."""

    async def test_event_to_dict_serialization(self):
        """Test converting event to dictionary."""
        from apps.backend.app.modules.justice.domain.events import CitizenCreated

        event = CitizenCreated(
            aggregate_id=uuid4(),
            aggregate_type="Citizen",
            event_type="CitizenCreated",
            first_name="Gonçalo",
            last_name="Martins",
            birth_date=date(1992, 7, 25),
            birth_place="Guarda",
            nationality="PT",
            correlation_id=uuid4(),
        )

        event_dict = event.to_dict()

        assert event_dict["aggregate_type"] == "Citizen"
        assert event_dict["first_name"] == "Gonçalo"
        assert isinstance(event_dict["aggregate_id"], str)  # UUID as string
        assert isinstance(event_dict["timestamp"], str)  # ISO format

    async def test_event_from_dict_deserialization(self):
        """Test reconstructing event from dictionary."""
        from apps.backend.app.modules.justice.domain.events import CitizenCreated

        original_id = uuid4()
        event_id = uuid4()

        event_dict = {
            "aggregate_id": str(original_id),
            "aggregate_type": "Citizen",
            "event_type": "CitizenCreated",
            "first_name": "Helena",
            "last_name": "Ribeiro",
            "birth_date": "1988-09-12",
            "birth_place": "Braga",
            "nationality": "PT",
            "event_id": str(event_id),
            "timestamp": "2023-03-14T10:30:00+00:00",
            "version": 1,
            "metadata": {},
            "correlation_id": None,
            "causation_id": None,
        }

        # Deserialize to CitizenCreated event class
        event = CitizenCreated.from_dict(event_dict)

        assert event.aggregate_id == original_id
        assert event.event_id == event_id
        assert event.first_name == "Helena"
        assert event.last_name == "Ribeiro"
        assert event.birth_place == "Braga"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
