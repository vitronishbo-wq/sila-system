"""
Integration Tests for PostgreSQL EventStore
Tests persistence and retrieval of domain events in PostgreSQL
"""

import pytest
import pytest_asyncio
from datetime import date
from uuid import uuid4

from app.infrastructure.event_sourcing import PostgreSQLEventStore
from app.infrastructure.event_sourcing.initialization import (
    init_event_store,
    drop_event_store,
)
from app.infrastructure.event_sourcing.registry import register_events
from app.modules.justice.domain.events import (
    CitizenCreated,
    CitizenIdentityDocumentIssued,
)


@pytest.mark.asyncio
class TestPostgreSQLEventStore:
    """Test PostgreSQL-backed event store."""
    
    @pytest_asyncio.fixture
    async def event_store(self):
        """Fixture: Initialize event store with database."""
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy.ext.asyncio import AsyncSession
        from sqlalchemy.ext.asyncio import create_async_engine
        import os
        
        # Initialize event registry for deserialization
        register_events()
        
        # Get DATABASE_URL from environment
        db_url = os.environ.get(
            "DATABASE_URL",
            "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@localhost:5432/sila_db"
        )
        
        # Create engine
        engine = create_async_engine(
            db_url,
            echo=False,
            pool_pre_ping=True,
        )
        
        # Create session factory
        session_factory = sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        
        # Initialize schema
        async with session_factory() as session:
            try:
                await init_event_store(session)
            except Exception as e:
                print(f"Warning: Could not initialize event store schema: {e}")
        
        # Create event store
        store = PostgreSQLEventStore(session_factory)
        
        yield store
        
        # Cleanup
        try:
            async with session_factory() as session:
                await drop_event_store(session)
        except Exception:
            pass
        
        await engine.dispose()
    
    async def test_append_single_event(self, event_store):
        """Test appending a single event to PostgreSQL."""
        citizen_id = uuid4()
        event = CitizenCreated(
            aggregate_id=citizen_id,
            aggregate_type="Citizen",
            event_type="CitizenCreated",
            first_name="João",
            last_name="Silva",
            birth_date=date(1990, 1, 15),
            birth_place="Lisbon",
            nationality="PT"
        )
        
        await event_store.append(event)
        
        # Retrieve and verify
        stored_events = await event_store.get_events_for_aggregate(citizen_id)
        assert len(stored_events) == 1
        assert stored_events[0].aggregate_id == citizen_id
        assert stored_events[0].first_name == "João"
    
    async def test_append_batch_of_events(self, event_store):
        """Test appending multiple events atomically."""
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
                nationality="PT"
            ),
            CitizenIdentityDocumentIssued(
                aggregate_id=citizen_id,
                aggregate_type="Citizen",
                event_type="CitizenIdentityDocumentIssued",
                document_number="12345678",
                document_type="ID_CARD",
                issue_date=date(2023, 1, 1),
                issuing_authority="IRN"
            )
        ]
        
        await event_store.append_batch(events)
        
        # Retrieve and verify
        stored_events = await event_store.get_events_for_aggregate(citizen_id)
        assert len(stored_events) == 2
        assert stored_events[0].event_type == "CitizenCreated"
        assert stored_events[1].event_type == "CitizenIdentityDocumentIssued"
    
    async def test_get_events_by_type(self, event_store):
        """Test retrieving events by type (compliance queries)."""
        citizen_id_1 = uuid4()
        citizen_id_2 = uuid4()
        
        # Create events for two citizens
        await event_store.append(CitizenCreated(
            aggregate_id=citizen_id_1,
            aggregate_type="Citizen",
            event_type="CitizenCreated",
            first_name="Alice",
            last_name="Johnson",
            birth_date=date(1990, 1, 1),
            birth_place="Lisbon",
            nationality="PT"
        ))
        
        await event_store.append(CitizenCreated(
            aggregate_id=citizen_id_2,
            aggregate_type="Citizen",
            event_type="CitizenCreated",
            first_name="Bob",
            last_name="Smith",
            birth_date=date(1995, 2, 2),
            birth_place="Porto",
            nationality="PT"
        ))
        
        # Query by event type
        created_events = await event_store.get_events_by_type("CitizenCreated")
        assert len(created_events) == 2
        assert all(e.event_type == "CitizenCreated" for e in created_events)
    
    async def test_get_event_by_id(self, event_store):
        """Test retrieving a specific event by ID."""
        citizen_id = uuid4()
        event = CitizenCreated(
            aggregate_id=citizen_id,
            aggregate_type="Citizen",
            event_type="CitizenCreated",
            first_name="Carlos",
            last_name="Oliveira",
            birth_date=date(2000, 1, 1),
            birth_place="Covilhã",
            nationality="PT"
        )
        
        await event_store.append(event)
        
        # Retrieve by event ID
        retrieved = await event_store.get_event_by_id(event.event_id)
        assert retrieved is not None
        assert retrieved.event_id == event.event_id
        assert retrieved.first_name == "Carlos"
    
    async def test_get_all_events_with_limit(self, event_store):
        """Test retrieving all events with limit."""
        # Create multiple events
        for i in range(5):
            citizen_id = uuid4()
            await event_store.append(CitizenCreated(
                aggregate_id=citizen_id,
                aggregate_type="Citizen",
                event_type="CitizenCreated",
                first_name=f"Person{i}",
                last_name="Test",
                birth_date=date(2000 + i, 1, 1),
                birth_place="Lisbon",
                nationality="PT"
            ))
        
        # Retrieve with limit
        events = await event_store.get_all_events(limit=3)
        assert len(events) == 3
    
    async def test_events_persisted_across_sessions(self, event_store):
        """Test that events persist across different sessions."""
        citizen_id = uuid4()
        event = CitizenCreated(
            aggregate_id=citizen_id,
            aggregate_type="Citizen",
            event_type="CitizenCreated",
            first_name="Diana",
            last_name="Costa",
            birth_date=date(2001, 3, 3),
            birth_place="Aveiro",
            nationality="PT"
        )
        
        # Store event
        await event_store.append(event)
        
        # Retrieve in "new session"
        stored_events = await event_store.get_events_for_aggregate(citizen_id)
        assert len(stored_events) == 1
        assert stored_events[0].first_name == "Diana"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
