"""Domain exceptions for Pescas module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Pescas')
PescasException = exc.Base
PescasNotFound = exc.NotFound
PescasValidationError = exc.ValidationError
PescasInvalidStateError = exc.InvalidStateError
__all__ = ['PescasException', 'PescasNotFound', 'PescasValidationError', 'PescasInvalidStateError']