"""
Auto-generated exceptions for PublicSecurity module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('PublicSecurity')
PublicSecurityException = _exc.Base
PublicSecurityNotFound = _exc.NotFound
PublicSecurityValidationError = _exc.ValidationError
PublicSecurityUnauthorized = _exc.Unauthorized
PublicSecurityConflict = _exc.Conflict
PublicSecurityInvalidState = _exc.InvalidState
PublicSecurityInvalidStateError = _exc.InvalidStateError