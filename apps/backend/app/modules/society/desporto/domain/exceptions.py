"""Domain exceptions for Desporto module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Desporto')
DesportoException = exc.Base
DesportoNotFound = exc.NotFound
DesportoValidationError = exc.ValidationError
DesportoInvalidStateError = exc.InvalidStateError
__all__ = ['DesportoException', 'DesportoNotFound', 'DesportoValidationError', 'DesportoInvalidStateError']