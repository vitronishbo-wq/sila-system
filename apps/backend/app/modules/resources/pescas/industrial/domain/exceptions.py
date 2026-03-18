"""Domain exceptions for Industrial module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Industrial')
IndustrialException = exc.Base
IndustrialNotFound = exc.NotFound
IndustrialValidationError = exc.ValidationError
IndustrialInvalidStateError = exc.InvalidStateError
__all__ = ['IndustrialException', 'IndustrialNotFound', 'IndustrialValidationError', 'IndustrialInvalidStateError']