"""Domain exceptions for Deprecated module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Deprecated')
DeprecatedException = exc.Base
DeprecatedNotFound = exc.NotFound
DeprecatedValidationError = exc.ValidationError
DeprecatedInvalidStateError = exc.InvalidStateError
__all__ = ['DeprecatedException', 'DeprecatedNotFound', 'DeprecatedValidationError', 'DeprecatedInvalidStateError']