"""Domain exceptions for Ambiente module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Ambiente')
AmbienteException = exc.Base
AmbienteNotFound = exc.NotFound
AmbienteValidationError = exc.ValidationError
AmbienteInvalidStateError = exc.InvalidStateError
__all__ = ['AmbienteException', 'AmbienteNotFound', 'AmbienteValidationError', 'AmbienteInvalidStateError']