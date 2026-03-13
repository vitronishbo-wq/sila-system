"""User-related domain events (login, logout, password changes)."""
from .event import DomainEvent

class UserLoggedIn(DomainEvent):
    """Event published when a user successfully logs in.
    
    This event is triggered after authentication succeeds and can be
    subscribed to by other services for:
    - Audit trails
    - Session tracking
    - Cross-service notifications
    - Analytics
    
    Example:
        ```python
        event = UserLoggedIn(
            user_id="user_123",
            request_id="req_456"
        )
        await EventBus.publish(event)
        ```
    """

    def __init__(self, user_id: str, request_id: str, **kwargs):
        """Initialize USER_LOGGED_IN event.
        
        Args:
            user_id: The user who logged in
            request_id: Request correlation ID from observability context
            **kwargs: Additional metadata
        """
        super().__init__(name='USER_LOGGED_IN', payload={'user_id': user_id}, metadata={'request_id': request_id, **kwargs})

class UserLoggedOut(DomainEvent):
    """Event published when a user logs out."""

    def __init__(self, user_id: str, request_id: str, **kwargs):
        super().__init__(name='USER_LOGGED_OUT', payload={'user_id': user_id}, metadata={'request_id': request_id, **kwargs})

class UserPasswordChanged(DomainEvent):
    """Event published when a user changes their password."""

    def __init__(self, user_id: str, request_id: str, **kwargs):
        super().__init__(name='USER_PASSWORD_CHANGED', payload={'user_id': user_id}, metadata={'request_id': request_id, **kwargs})