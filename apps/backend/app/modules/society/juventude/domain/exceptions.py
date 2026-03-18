"""Domain exceptions for Juventude module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Juventude')
JuventudeException = exc.Base
JuventudeNotFound = exc.NotFound
JuventudeValidationError = exc.ValidationError
JuventudeInvalidStateError = exc.InvalidStateError
__all__ = ['JuventudeException', 'JuventudeNotFound', 'JuventudeValidationError', 'JuventudeInvalidStateError']