"""Event bus configuration."""
from enum import Enum

class BrokerType(Enum):
    """Supported message brokers."""
    REDIS = 'redis'
    KAFKA = 'kafka'
    MEMORY = 'memory'

class EventBusConfig:
    """Configuration for event bus behavior.
    
    Attributes:
        broker_type: Which broker to use (Redis, Kafka, etc.)
        retry_policy: How to handle failed handler executions
        timeout_seconds: Timeout for handler execution
        batch_size: Number of events to batch if applicable
        persistence: Whether to persist events for audit trail
    """

    def __init__(self, broker_type: BrokerType=BrokerType.REDIS, retry_policy: str='none', timeout_seconds: int=30, batch_size: int=100, persistence: bool=True):
        self.broker_type = broker_type
        self.retry_policy = retry_policy
        self.timeout_seconds = timeout_seconds
        self.batch_size = batch_size
        self.persistence = persistence