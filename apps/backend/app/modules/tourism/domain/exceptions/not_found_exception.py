"""Entity not found exception"""
from typing import Any
from apps.backend.core.exceptions.domain_exception import DomainException

class EntityNotFoundException(DomainException):
    """
    Raised when an entity is not found in repository.
    
    Used for:
    - Repository queries returning no results
    - Lookup failures by ID or unique fields
    - Aggregates not found in store
    """

    def __init__(self, entity_type: str, entity_id: Any):
        """
        Initialize entity not found exception.
        
        Args:
            entity_type: Name of entity type (e.g., "User", "Order")
            entity_id: ID or identifier of missing entity
        """
        message = f"{entity_type} with ID '{entity_id}' not found"
        super().__init__(message=message, code='ENTITY_NOT_FOUND', context={'entity_type': entity_type, 'entity_id': str(entity_id)})

class AggregateNotFoundException(DomainException):
    """
    Raised when an aggregate root is not found.
    
    Specialization of EntityNotFoundException for aggregate roots.
    """

    def __init__(self, aggregate_type: str, aggregate_id: Any):
        """
        Initialize aggregate not found exception.
        
        Args:
            aggregate_type: Name of aggregate root (e.g., "Order", "Customer")
            aggregate_id: ID of missing aggregate
        """
        message = f"Aggregate {aggregate_type} with ID '{aggregate_id}' not found"
        super().__init__(message=message, code='AGGREGATE_NOT_FOUND', context={'aggregate_type': aggregate_type, 'aggregate_id': str(aggregate_id)})
__all__ = ['EntityNotFoundException', 'AggregateNotFoundException']