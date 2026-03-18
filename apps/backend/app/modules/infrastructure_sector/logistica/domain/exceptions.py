"""Domain exceptions for Logistica module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Logistica')
LogisticaException = exc.Base
LogisticaNotFound = exc.NotFound
LogisticaValidationError = exc.ValidationError
LogisticaInvalidStateError = exc.InvalidStateError
__all__ = ['LogisticaException', 'LogisticaNotFound', 'LogisticaValidationError', 'LogisticaInvalidStateError']