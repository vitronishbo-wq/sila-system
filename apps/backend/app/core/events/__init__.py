"""Core eventing package."""
import importlib.util
import sys
from pathlib import Path
bus_file = Path(__file__).parent / 'bus.py'
spec = importlib.util.spec_from_file_location('_bus_module', bus_file)
_bus_module = importlib.util.module_from_spec(spec)
sys.modules['_bus_module'] = _bus_module
spec.loader.exec_module(_bus_module)
EventBus = _bus_module.EventBus
EventPublisher = _bus_module.EventPublisher
get_event_bus = _bus_module.get_event_bus
get_events_by_type = _bus_module.get_events_by_type
get_recent_events = _bus_module.get_recent_events
store_event = _bus_module.store_event
from .types import CitizenValidated, CitizenValidationFailed, DomainEvent
from .bus_enhanced import EventBus as EnhancedEventBus
from .broker import RedisBroker
from .handlers import EventHandler
from .registry import HandlerRegistry
from .models import UserLoggedIn, UserLoggedOut, UserPasswordChanged
from .decorators import publish_event
from .config import EventBusConfig, BrokerType
from .ports import EventBusPort
from .adapters import EventBusAdapter
from .exceptions import EventBusException, BrokerConnectionError, PublishFailedError, SubscriptionError, HandlerExecutionError
__all__ = ['CitizenValidated', 'CitizenValidationFailed', 'DomainEvent', 'EventBus', 'EventPublisher', 'get_event_bus', 'get_events_by_type', 'get_recent_events', 'store_event', 'EnhancedEventBus', 'RedisBroker', 'EventHandler', 'HandlerRegistry', 'UserLoggedIn', 'UserLoggedOut', 'UserPasswordChanged', 'publish_event', 'EventBusConfig', 'BrokerType', 'EventBusPort', 'EventBusAdapter', 'EventBusException', 'BrokerConnectionError', 'PublishFailedError', 'SubscriptionError', 'HandlerExecutionError']