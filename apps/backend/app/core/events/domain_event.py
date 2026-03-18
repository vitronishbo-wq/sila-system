"""
Domain Events - Core event infrastructure for event sourcing and audit compliance.
Follows ACAO compliance requirements for official status tracking.
"""
from abc import ABC
from dataclasses import dataclass, field, asdict, fields
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

@dataclass
class DomainEvent(ABC):
    """
    Base class for all domain events.
    
    Attributes:
        event_id: Unique event identifier (UUID)
        aggregate_id: ID of the aggregate that produced this event
        aggregate_type: Type of the aggregate (e.g., "Citizen", "Payment")
        event_type: Type of event (e.g., "CitizenCreated", "PaymentProcessed")
        timestamp: When the event occurred (UTC)
        version: Event version for schema evolution
        metadata: Additional context (user_id, request_id, etc.)
        correlation_id: For tracing related events across modules
        causation_id: Links to triggering command/event
    """
    aggregate_id: UUID
    aggregate_type: str
    event_type: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    version: int = 1
    event_id: UUID = field(default_factory=uuid4)
    metadata: Dict[str, Any] = field(default_factory=dict)
    correlation_id: Optional[UUID] = None
    causation_id: Optional[UUID] = None

    def __post_init__(self):
        """Validate event structure."""
        if not self.aggregate_id:
            raise ValueError('aggregate_id is required')
        if not self.aggregate_type:
            raise ValueError('aggregate_type is required')
        if not self.event_type:
            raise ValueError('event_type is required')

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary for serialization."""
        data = asdict(self)
        data['event_id'] = str(self.event_id)
        data['aggregate_id'] = str(self.aggregate_id)
        if self.correlation_id:
            data['correlation_id'] = str(self.correlation_id)
        if self.causation_id:
            data['causation_id'] = str(self.causation_id)
        data['timestamp'] = self.timestamp.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DomainEvent':
        """Reconstruct event from dictionary (deserialization)."""
        data_copy = data.copy()
        data_copy['event_id'] = UUID(data_copy['event_id']) if isinstance(data_copy.get('event_id'), str) else data_copy.get('event_id')
        data_copy['aggregate_id'] = UUID(data_copy['aggregate_id']) if isinstance(data_copy.get('aggregate_id'), str) else data_copy.get('aggregate_id')
        if data_copy.get('correlation_id'):
            data_copy['correlation_id'] = UUID(data_copy['correlation_id']) if isinstance(data_copy['correlation_id'], str) else data_copy['correlation_id']
        if data_copy.get('causation_id'):
            data_copy['causation_id'] = UUID(data_copy['causation_id']) if isinstance(data_copy['causation_id'], str) else data_copy['causation_id']
        if isinstance(data_copy.get('timestamp'), str):
            data_copy['timestamp'] = datetime.fromisoformat(data_copy['timestamp'])
        valid_fields = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data_copy.items() if k in valid_fields}
        return cls(**filtered_data)

class AuditableEvent(DomainEvent):
    """Base class for events that require audit trail compliance."""
    pass

class ComplianceEvent(DomainEvent):
    """Base class for ACAO compliance-related events."""
    pass

class StatusChangeEvent(DomainEvent):
    """Base class for status transition events."""
    old_status: Optional[str] = None
    new_status: str = ''

    def __post_init__(self):
        super().__post_init__()
        if not self.new_status:
            raise ValueError('new_status is required for StatusChangeEvent')