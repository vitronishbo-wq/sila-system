"""
Common exceptions for the SILA system.

This module defines all custom exceptions used across modules in the SILA system.
Provides a consistent error handling approach with standardized error codes and messages.
"""

from typing import Any, Dict, Optional, Union

from fastapi import status
from fastapi.exceptions import HTTPException


class SILAError(Exception):
    """Base exception for all SILA-related errors."""

    def __init__(
        self,
        message: str,
        code: str = "sila_error",
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(message)


class ResourceNotFoundError(SILAError):
    """Raised when a resource is not found."""

    def __init__(
        self, resource_type: str, resource_id: Optional[Union[int, str]] = None
    ):
        message = f"{resource_type} not found"
        if resource_id is not None:
            message += f" with ID: {resource_id}"
        super().__init__(
            message,
            "resource_not_found",
            {"resource_type": resource_type, "resource_id": resource_id},
        )


class DuplicateResourceError(SILAError):
    """Raised when trying to create a resource that already exists."""

    def __init__(
        self, resource_type: str, identifier: str, identifier_type: str = "ID"
    ):
        super().__init__(
            f"{resource_type} with {identifier_type} '{identifier}' already exists",
            "duplicate_resource",
            {
                "resource_type": resource_type,
                "identifier": identifier,
                "identifier_type": identifier_type,
            },
        )


class ValidationError(SILAError):
    """Raised when validation fails."""

    def __init__(self, details: str, field: Optional[str] = None):
        super().__init__(
            f"Validation failed: {details}",
            "validation_error",
            {"details": details, "field": field},
        )


class BusinessRuleError(SILAError):
    """Raised when a business rule is violated."""

    def __init__(self, rule: str, details: str):
        super().__init__(
            f"Business rule violation: {rule} - {details}",
            "business_rule_error",
            {"rule": rule, "details": details},
        )


class AuthenticationError(SILAError):
    """Raised when authentication fails."""

    def __init__(self, details: str = "Invalid credentials"):
        super().__init__(details, "authentication_error")


class AuthorizationError(SILAError):
    """Raised when authorization fails."""

    def __init__(self, action: str, resource: Optional[str] = None):
        message = f"Not authorized to perform action: {action}"
        if resource:
            message += f" on resource: {resource}"
        super().__init__(
            message, "authorization_error", {"action": action, "resource": resource}
        )


class DatabaseError(SILAError):
    """Raised when database operation fails."""

    def __init__(self, operation: str, details: Optional[str] = None):
        message = f"Database operation failed: {operation}"
        if details:
            message += f" - {details}"
        super().__init__(
            message, "database_error", {"operation": operation, "details": details}
        )


class ExternalServiceError(SILAError):
    """Raised when external service call fails."""

    def __init__(self, service: str, details: Optional[str] = None):
        message = f"External service error: {service}"
        if details:
            message += f" - {details}"
        super().__init__(
            message, "external_service_error", {"service": service, "details": details}
        )


class ConfigurationError(SILAError):
    """Raised when configuration is invalid."""

    def __init__(self, config_key: str, details: Optional[str] = None):
        message = f"Configuration error: {config_key}"
        if details:
            message += f" - {details}"
        super().__init__(
            message,
            "configuration_error",
            {"config_key": config_key, "details": details},
        )


def handle_sila_error(error: SILAError) -> HTTPException:
    """Convert a SILAError to an HTTPException.

    Args:
        error: The SILAError to convert.

    Returns:
        HTTPException: The corresponding HTTP exception.
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    if isinstance(error, ResourceNotFoundError):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(error, DuplicateResourceError):
        status_code = status.HTTP_409_CONFLICT
    elif isinstance(error, ValidationError):
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    elif isinstance(error, (AuthenticationError, AuthorizationError)):
        status_code = (
            status.HTTP_401_UNAUTHORIZED
            if isinstance(error, AuthenticationError)
            else status.HTTP_403_FORBIDDEN
        )
    elif isinstance(error, BusinessRuleError):
        status_code = status.HTTP_400_BAD_REQUEST
    elif isinstance(error, DatabaseError):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    elif isinstance(error, ExternalServiceError):
        status_code = status.HTTP_502_BAD_GATEWAY
    elif isinstance(error, ConfigurationError):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return HTTPException(
        status_code=status_code,
        detail={
            "code": error.code,
            "message": str(error),
            "type": error.__class__.__name__,
            "details": error.details,
        },
    )


# Export all exceptions
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
