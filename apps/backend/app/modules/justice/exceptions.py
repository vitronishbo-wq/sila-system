"""
Auto-generated exceptions for Justice module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('Justice')
JusticeException = _exc.Base
JusticeNotFound = _exc.NotFound
JusticeValidationError = _exc.ValidationError
JusticeUnauthorized = _exc.Unauthorized
JusticeConflict = _exc.Conflict
JusticeInvalidState = _exc.InvalidState
JusticeInvalidStateError = _exc.InvalidStateError