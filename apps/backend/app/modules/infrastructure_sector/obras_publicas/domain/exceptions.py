"""Domain exceptions for ObrasPublicas module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('ObrasPublicas')
ObrasPublicasException = exc.Base
ObrasPublicasNotFound = exc.NotFound
ObrasPublicasValidationError = exc.ValidationError
ObrasPublicasInvalidStateError = exc.InvalidStateError
__all__ = ['ObrasPublicasException', 'ObrasPublicasNotFound', 'ObrasPublicasValidationError', 'ObrasPublicasInvalidStateError']