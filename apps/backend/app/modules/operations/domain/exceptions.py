"""
Auto-generated exceptions for Operations module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('Operations')
OperationsException = _exc.Base
OperationsNotFound = _exc.NotFound
OperationsValidationError = _exc.ValidationError
OperationsUnauthorized = _exc.Unauthorized
OperationsConflict = _exc.Conflict
OperationsInvalidState = _exc.InvalidState
OperationsInvalidStateError = _exc.InvalidStateError