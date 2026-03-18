"""Domain exceptions for Services module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Services')
ServicesException = exc.Base
ServicesNotFound = exc.NotFound
ServicesValidationError = exc.ValidationError
ServicesInvalidStateError = exc.InvalidStateError
__all__ = ['ServicesException', 'ServicesNotFound', 'ServicesValidationError', 'ServicesInvalidStateError']