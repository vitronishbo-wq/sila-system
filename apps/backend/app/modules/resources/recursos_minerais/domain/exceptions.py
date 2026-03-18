"""Domain exceptions for RecursosMinerais module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('RecursosMinerais')
RecursosMineraisException = exc.Base
RecursosMineraisNotFound = exc.NotFound
RecursosMineraisValidationError = exc.ValidationError
RecursosMineraisInvalidStateError = exc.InvalidStateError
__all__ = ['RecursosMineraisException', 'RecursosMineraisNotFound', 'RecursosMineraisValidationError', 'RecursosMineraisInvalidStateError']