"""
Auto-generated exceptions for Xroad module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('Xroad')
XroadException = _exc.Base
XroadNotFound = _exc.NotFound
XroadValidationError = _exc.ValidationError
XroadUnauthorized = _exc.Unauthorized
XroadConflict = _exc.Conflict
XroadInvalidState = _exc.InvalidState
XroadInvalidStateError = _exc.InvalidStateError