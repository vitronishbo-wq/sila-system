"""Base domain event class."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, Any

@dataclass(slots=True)
class DomainEvent:
    """Base class for all domain events in SILA.
    
    Every event that flows through the Event Bus should inherit from this class.
    Provides automatic correlation, tracing, and observability integration.
    
    Attributes:
        name: Event type identifier (e.g., "USER_LOGGED_IN")
        payload: Event data as key-value pairs
        id: Unique event identifier (auto-generated)
        occurred_at: Timestamp when event occurred (auto-generated)
        version: Event schema version for backward compatibility
        metadata: Additional context (request_id, trace_id, etc.)
    
    Example:
        ```python
        event = UserLoggedIn(
            user_id="user_123",
            request_id="req_456"
        )
        await EventBus.publish(event)
        ```
    """
    name: str
    payload: Dict[str, Any]
    id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    version: str = '1.0'
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Ensure payload is properly initialized."""
        if self.payload is None:
            self.payload = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary for serialization.
        
        Returns:
            dict: Event as dictionary with all fields
        """
        return {'name': self.name, 'payload': self.payload, 'id': self.id, 'occurred_at': self.occurred_at.isoformat(), 'version': self.version, 'metadata': self.metadata}