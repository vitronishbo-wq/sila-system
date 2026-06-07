"""Unified ValidationException hierarchy"""

from apps.backend.app.core.exceptions import DomainException


class ValidationException(DomainException):
    """Domain validation failed"""

    def __init__(self, field: str = None, message: str = None, code: str = "VALIDATION_ERROR", context: dict = None):
        if field and not message:
            message = f"Validation failed for field: {field}"
        elif not message:
            message = "Validation error"
        super().__init__(message=message, code=code, context=context or {"field": field})


__all__ = ["ValidationException"]
