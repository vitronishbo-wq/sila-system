"""Domain exceptions for Events module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Events')
EventsException = exc.Base
EventsNotFound = exc.NotFound
EventsValidationError = exc.ValidationError
EventsInvalidStateError = exc.InvalidStateError
__all__ = ['EventsException', 'EventsNotFound', 'EventsValidationError', 'EventsInvalidStateError']