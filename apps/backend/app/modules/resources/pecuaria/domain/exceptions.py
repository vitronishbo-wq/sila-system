"""Domain exceptions for Pecuaria module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Pecuaria')
PecuariaException = exc.Base
PecuariaNotFound = exc.NotFound
PecuariaValidationError = exc.ValidationError
PecuariaInvalidStateError = exc.InvalidStateError
__all__ = ['PecuariaException', 'PecuariaNotFound', 'PecuariaValidationError', 'PecuariaInvalidStateError']