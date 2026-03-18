"""Domain exceptions for Familia module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Familia')
FamiliaException = exc.Base
FamiliaNotFound = exc.NotFound
FamiliaValidationError = exc.ValidationError
FamiliaInvalidStateError = exc.InvalidStateError
__all__ = ['FamiliaException', 'FamiliaNotFound', 'FamiliaValidationError', 'FamiliaInvalidStateError']