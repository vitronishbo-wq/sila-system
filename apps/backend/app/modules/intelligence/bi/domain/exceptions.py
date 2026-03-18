"""Domain exceptions for Bi module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Bi')
BiException = exc.Base
BiNotFound = exc.NotFound
BiValidationError = exc.ValidationError
BiInvalidStateError = exc.InvalidStateError
__all__ = ['BiException', 'BiNotFound', 'BiValidationError', 'BiInvalidStateError']