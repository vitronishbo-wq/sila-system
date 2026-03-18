"""
Auto-generated exceptions for Resources module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('Resources')
ResourcesException = _exc.Base
ResourcesNotFound = _exc.NotFound
ResourcesValidationError = _exc.ValidationError
ResourcesUnauthorized = _exc.Unauthorized
ResourcesConflict = _exc.Conflict
ResourcesInvalidState = _exc.InvalidState
ResourcesInvalidStateError = _exc.InvalidStateError