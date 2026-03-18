"""
Auto-generated exceptions for Identity module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('Identity')
IdentityException = _exc.Base
IdentityNotFound = _exc.NotFound
IdentityValidationError = _exc.ValidationError
IdentityUnauthorized = _exc.Unauthorized
IdentityConflict = _exc.Conflict
IdentityInvalidState = _exc.InvalidState
IdentityInvalidStateError = _exc.InvalidStateError