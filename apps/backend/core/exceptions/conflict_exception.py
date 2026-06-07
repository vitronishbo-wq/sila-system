"""Unified ConflictException hierarchy"""

from apps.backend.app.core.exceptions import DomainException


class ConflictException(DomainException):
    """Resource conflict (already exists, state mismatch, etc)"""

    def __init__(self, resource: str = None, reason: str = None, code: str = "CONFLICT", context: dict = None):
        message = f"Conflict: {reason or 'Resource already exists'}"
        if resource:
            message += f" ({resource})"
        super().__init__(message=message, code=code, context=context or {})


__all__ = ["ConflictException"]
