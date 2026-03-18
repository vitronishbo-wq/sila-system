"""Domain exceptions for Emprego module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Emprego')
EmpregoException = exc.Base
EmpregoNotFound = exc.NotFound
EmpregoValidationError = exc.ValidationError
EmpregoInvalidStateError = exc.InvalidStateError
__all__ = ['EmpregoException', 'EmpregoNotFound', 'EmpregoValidationError', 'EmpregoInvalidStateError']