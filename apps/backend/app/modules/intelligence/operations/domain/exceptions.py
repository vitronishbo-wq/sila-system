"""Domain exceptions for Operations module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Operations')
OperationsException = exc.Base
OperationsNotFound = exc.NotFound
OperationsValidationError = exc.ValidationError
OperationsInvalidStateError = exc.InvalidStateError
__all__ = ['OperationsException', 'OperationsNotFound', 'OperationsValidationError', 'OperationsInvalidStateError']