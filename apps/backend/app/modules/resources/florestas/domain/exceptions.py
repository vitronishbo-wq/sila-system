"""Domain exceptions for Florestas module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Florestas')
FlorestasException = exc.Base
FlorestasNotFound = exc.NotFound
FlorestasValidationError = exc.ValidationError
FlorestasInvalidStateError = exc.InvalidStateError
__all__ = ['FlorestasException', 'FlorestasNotFound', 'FlorestasValidationError', 'FlorestasInvalidStateError']