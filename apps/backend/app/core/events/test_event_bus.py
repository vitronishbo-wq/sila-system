"""Tests for Event-Driven Architecture implementation."""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
import json
from app.core.events.models import DomainEvent, UserLoggedIn
from app.core.events.handlers import EventHandler
from app.core.events.registry import HandlerRegistry
from app.core.events.broker import RedisBroker
from app.core.events.bus_enhanced import EventBus

class TestEventModels:
    """Test domain event models."""

    def test_domain_event_creation(self):
        """Test creating a domain event."""
        event = DomainEvent(name='TEST_EVENT', payload={'key': 'value'})
        assert event.name == 'TEST_EVENT'
        assert event.payload == {'key': 'value'}
        assert event.id is not None
        assert event.occurred_at is not None
        assert event.version == '1.0'

    def test_user_logged_in_event(self):
        """Test USER_LOGGED_IN event."""
        event = UserLoggedIn(user_id='user_123', request_id='req_456')
        assert event.name == 'USER_LOGGED_IN'
        assert event.payload['user_id'] == 'user_123'
        assert event.metadata['request_id'] == 'req_456'

    def test_event_to_dict(self):
        """Test event serialization to dict."""
        event = UserLoggedIn(user_id='user_123', request_id='req_456')
        event_dict = event.to_dict()
        assert event_dict['name'] == 'USER_LOGGED_IN'
        assert event_dict['payload']['user_id'] == 'user_123'
        assert 'id' in event_dict
        assert 'occurred_at' in event_dict

class TestEventHandler:
    """Test event handler implementation."""

    def test_handler_creation(self):
        """Test creating a concrete event handler."""

        class TestHandler(EventHandler):

            async def handle(self, event):
                pass
        handler = TestHandler()
        assert hasattr(handler, 'handle')

    @pytest.mark.asyncio
    async def test_handler_execution(self):
        """Test handler can be executed."""
        handled_events = []

        class TestHandler(EventHandler):

            async def handle(self, event):
                handled_events.append(event.name)
        handler = TestHandler()
        event = UserLoggedIn(user_id='user_123', request_id='req_456')
        await handler.handle(event)
        assert 'USER_LOGGED_IN' in handled_events

class TestHandlerRegistry:
    """Test handler registry."""

    def setup_method(self):
        """Clear registry before each test."""
        HandlerRegistry.clear()

    def test_register_handler(self):
        """Test registering a handler."""

        class TestHandler(EventHandler):

            async def handle(self, event):
                pass
        handler = TestHandler()
        HandlerRegistry.register('TEST_EVENT', handler)
        handlers = HandlerRegistry.get('TEST_EVENT')
        assert len(handlers) == 1
        assert handlers[0] is handler

    def test_register_multiple_handlers(self):
        """Test registering multiple handlers for same event."""

        class Handler1(EventHandler):

            async def handle(self, event):
                pass

        class Handler2(EventHandler):

            async def handle(self, event):
                pass
        h1 = Handler1()
        h2 = Handler2()
        HandlerRegistry.register('TEST_EVENT', h1)
        HandlerRegistry.register('TEST_EVENT', h2)
        handlers = HandlerRegistry.get('TEST_EVENT')
        assert len(handlers) == 2

    def test_get_nonexistent_event_handlers(self):
        """Test getting handlers for non-existent event returns empty list."""
        handlers = HandlerRegistry.get('NONEXISTENT')
        assert handlers == []

    def test_registry_stats(self):
        """Test registry statistics."""

        class Handler1(EventHandler):

            async def handle(self, event):
                pass
        h1 = Handler1()
        HandlerRegistry.register('EVENT1', h1)
        HandlerRegistry.register('EVENT2', h1)
        stats = HandlerRegistry.get_stats()
        assert stats['event_types'] == 2
        assert stats['total_handlers'] == 2

class TestEventBus:
    """Test event bus functionality."""

    def setup_method(self):
        """Setup before each test."""
        HandlerRegistry.clear()
        EventBus._initialized = False

    @patch('app.core.events.bus_enhanced.RedisBroker')
    def test_event_bus_initialization(self, mock_broker_class):
        """Test event bus initialization."""
        mock_broker = MagicMock()
        mock_broker_class.return_value = mock_broker
        EventBus.initialize()
        assert EventBus._initialized
        assert EventBus._broker is not None

    @patch('app.core.events.bus_enhanced.RedisBroker')
    @pytest.mark.asyncio
    async def test_publish_event(self, mock_broker_class):
        """Test publishing an event."""
        mock_broker = MagicMock()
        mock_broker.publish = AsyncMock()
        mock_broker_class.return_value = mock_broker
        EventBus.initialize(mock_broker)
        event = UserLoggedIn(user_id='user_123', request_id='req_456')
        await EventBus.publish(event)
        mock_broker.publish.assert_called_once()
        call_args = mock_broker.publish.call_args
        assert call_args[1]['channel'] == 'USER_LOGGED_IN'

    @patch('app.core.events.bus_enhanced.RedisBroker')
    @pytest.mark.asyncio
    async def test_dispatch_to_handlers(self, mock_broker_class):
        """Test dispatching event to handlers."""
        mock_broker = MagicMock()
        mock_broker.publish = AsyncMock()
        mock_broker_class.return_value = mock_broker
        handled_events = []

        class TestHandler(EventHandler):

            async def handle(self, event):
                handled_events.append(event.name)
        handler = TestHandler()
        HandlerRegistry.register('USER_LOGGED_IN', handler)
        EventBus.initialize(mock_broker)
        event = UserLoggedIn(user_id='user_123', request_id='req_456')
        await EventBus.dispatch(event)
        assert 'USER_LOGGED_IN' in handled_events

    @patch('app.core.events.bus_enhanced.RedisBroker')
    @pytest.mark.asyncio
    async def test_health_check(self, mock_broker_class):
        """Test event bus health check."""
        mock_broker = MagicMock()
        mock_broker.health_check = AsyncMock(return_value=True)
        mock_broker_class.return_value = mock_broker
        EventBus.initialize(mock_broker)
        health = await EventBus.health_check()
        assert health['status'] == 'healthy'
        assert health['broker']['name'] == 'Redis'
        assert health['broker']['healthy'] is True

class TestIntegration:
    """Integration tests for event-driven architecture."""

    def setup_method(self):
        """Setup before each test."""
        HandlerRegistry.clear()
        EventBus._initialized = False

    @patch('app.core.events.bus_enhanced.RedisBroker')
    @pytest.mark.asyncio
    async def test_full_event_flow(self, mock_broker_class):
        """Test complete event publishing and handling flow."""
        mock_broker = MagicMock()
        mock_broker.publish = AsyncMock()
        mock_broker_class.return_value = mock_broker
        handled_events = []

        class EducacaoHandler(EventHandler):

            async def handle(self, event):
                handled_events.append({'service': 'educacao', 'event': event.name, 'user_id': event.payload.get('user_id')})

        class TaxeHandler(EventHandler):

            async def handle(self, event):
                handled_events.append({'service': 'taxes', 'event': event.name, 'user_id': event.payload.get('user_id')})
        HandlerRegistry.register('USER_LOGGED_IN', EducacaoHandler())
        HandlerRegistry.register('USER_LOGGED_IN', TaxeHandler())
        EventBus.initialize(mock_broker)
        event = UserLoggedIn(user_id='user_456', request_id='req_789')
        await EventBus.publish(event)
        assert len(handled_events) == 2
        assert handled_events[0]['service'] == 'educacao'
        assert handled_events[1]['service'] == 'taxes'
        assert handled_events[0]['user_id'] == 'user_456'

class TestRedisIntegration:
    """Tests for Redis broker integration."""

    @pytest.mark.asyncio
    async def test_redis_broker_creation(self):
        """Test creating a Redis broker instance."""
        with patch('redis.asyncio.Redis.from_url') as mock_from_url:
            with patch.object(RedisBroker, '__init__', lambda self: None):
                broker = RedisBroker()
                assert broker is not None

    @pytest.mark.asyncio
    async def test_redis_broker_health_check(self):
        """Test Redis broker health check."""
        with patch('redis.asyncio.Redis.from_url'):
            broker = RedisBroker.__new__(RedisBroker)
            broker.client = AsyncMock()
            broker.client.ping = AsyncMock(return_value=True)
            health = await broker.health_check()
            assert health is True

def test_event_registry_isolation():
    """Test that event registry doesn't leak between tests."""
    HandlerRegistry.clear()

    class Handler1(EventHandler):

        async def handle(self, event):
            pass
    HandlerRegistry.register('EVENT', Handler1())
    initial_stats = HandlerRegistry.get_stats()
    HandlerRegistry.clear()
    cleared_stats = HandlerRegistry.get_stats()
    assert initial_stats['total_handlers'] > 0
    assert cleared_stats['total_handlers'] == 0
if __name__ == '__main__':
    pytest.main([__file__, '-v'])