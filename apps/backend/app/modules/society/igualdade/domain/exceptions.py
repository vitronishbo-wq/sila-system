"""Domain exceptions for Igualdade module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Igualdade')
IgualdadeException = exc.Base
IgualdadeNotFound = exc.NotFound
IgualdadeValidationError = exc.ValidationError
IgualdadeInvalidStateError = exc.InvalidStateError
__all__ = ['IgualdadeException', 'IgualdadeNotFound', 'IgualdadeValidationError', 'IgualdadeInvalidStateError']