"""Domain exceptions for Cultura module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Cultura')
CulturaException = exc.Base
CulturaNotFound = exc.NotFound
CulturaValidationError = exc.ValidationError
CulturaInvalidStateError = exc.InvalidStateError
__all__ = ['CulturaException', 'CulturaNotFound', 'CulturaValidationError', 'CulturaInvalidStateError']