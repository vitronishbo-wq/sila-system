"""Domain exceptions for Meteorologia module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Meteorologia')
MeteorologiaException = exc.Base
MeteorologiaNotFound = exc.NotFound
MeteorologiaValidationError = exc.ValidationError
MeteorologiaInvalidStateError = exc.InvalidStateError
__all__ = ['MeteorologiaException', 'MeteorologiaNotFound', 'MeteorologiaValidationError', 'MeteorologiaInvalidStateError']