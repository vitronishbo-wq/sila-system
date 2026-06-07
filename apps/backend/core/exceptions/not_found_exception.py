"""Unified NotFoundException hierarchy"""

from apps.backend.app.core.exceptions import DomainException


class NotFoundException(DomainException):
    """Entity not found in the system"""

    def __init__(self, entity_type: str, entity_id: str, code: str = "NOT_FOUND", context: dict = None):
        message = f"{entity_type} with id {entity_id} not found"
        super().__init__(message=message, code=code, context=context or {})


class EntityNotFoundException(NotFoundException):
    """Entity not found - backward compatibility alias"""
    pass


class AggregateNotFoundException(NotFoundException):
    """Aggregate root not found"""
    pass


__all__ = ["NotFoundException", "EntityNotFoundException", "AggregateNotFoundException"]
