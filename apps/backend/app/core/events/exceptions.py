"""Event bus exceptions."""

class EventBusException(Exception):
    """Base exception for event bus errors."""
    pass

class BrokerConnectionError(EventBusException):
    """Failed to connect to message broker."""
    pass

class PublishFailedError(EventBusException):
    """Failed to publish event."""
    pass

class SubscriptionError(EventBusException):
    """Failed to subscribe to event channel."""
    pass

class HandlerExecutionError(EventBusException):
    """Error during handler execution."""
    pass

class TimeoutError(EventBusException):
    """Handler execution timed out."""
    pass