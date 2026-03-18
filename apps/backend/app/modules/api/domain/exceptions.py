"""
Auto-generated exceptions for Api module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('Api')
ApiException = _exc.Base
ApiNotFound = _exc.NotFound
ApiValidationError = _exc.ValidationError
ApiUnauthorized = _exc.Unauthorized
ApiConflict = _exc.Conflict
ApiInvalidState = _exc.InvalidState
ApiInvalidStateError = _exc.InvalidStateError