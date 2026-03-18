"""Domain exceptions for External module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('External')
ExternalException = exc.Base
ExternalNotFound = exc.NotFound
ExternalValidationError = exc.ValidationError
ExternalInvalidStateError = exc.InvalidStateError
__all__ = ['ExternalException', 'ExternalNotFound', 'ExternalValidationError', 'ExternalInvalidStateError']