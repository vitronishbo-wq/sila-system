"""Unified exception module"""

from apps.backend.app.core.exceptions.conflict_exception import ConflictException
from apps.backend.app.core.exceptions.domain_exception import DomainException, DomainExceptionFactory
from apps.backend.app.core.exceptions.not_found_exception import (
    AggregateNotFoundException,
    EntityNotFoundException,
    NotFoundException,
)
from apps.backend.app.core.exceptions.validation_exception import ValidationException

__all__ = [
    "DomainException",
    "DomainExceptionFactory",
    "NotFoundException",
    "EntityNotFoundException",
    "AggregateNotFoundException",
    "ValidationException",
    "ConflictException",
]
