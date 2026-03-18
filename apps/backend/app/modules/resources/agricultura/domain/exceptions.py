"""Domain exceptions for Agricultura module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Agricultura')
AgriculturaException = exc.Base
AgriculturaNotFound = exc.NotFound
AgriculturaValidationError = exc.ValidationError
AgriculturaInvalidStateError = exc.InvalidStateError
__all__ = ['AgriculturaException', 'AgriculturaNotFound', 'AgriculturaValidationError', 'AgriculturaInvalidStateError']