"""
Auto-generated exceptions for Economy module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('Economy')
EconomyException = _exc.Base
EconomyNotFound = _exc.NotFound
EconomyValidationError = _exc.ValidationError
EconomyUnauthorized = _exc.Unauthorized
EconomyConflict = _exc.Conflict
EconomyInvalidState = _exc.InvalidState
EconomyInvalidStateError = _exc.InvalidStateError