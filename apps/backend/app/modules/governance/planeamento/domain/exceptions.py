"""Domain exceptions for Planeamento module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Planeamento')
PlaneamentoException = exc.Base
PlaneamentoNotFound = exc.NotFound
PlaneamentoValidationError = exc.ValidationError
PlaneamentoInvalidStateError = exc.InvalidStateError
__all__ = ['PlaneamentoException', 'PlaneamentoNotFound', 'PlaneamentoValidationError', 'PlaneamentoInvalidStateError']