"""Common exceptions module."""

from .exceptions import (
    SILAError,
    ResourceNotFoundError,
    DuplicateResourceError,
    ValidationError,
    BusinessRuleError,
    AuthenticationError,
    AuthorizationError,
    DatabaseError,
    ExternalServiceError,
    ConfigurationError,
    handle_sila_error,
)

__all__ = [
    "SILAError",
    "ResourceNotFoundError",
    "DuplicateResourceError",
    "ValidationError",
    "BusinessRuleError",
    "AuthenticationError",
    "AuthorizationError",
    "DatabaseError",
    "ExternalServiceError",
    "ConfigurationError",
    "handle_sila_error",
]
