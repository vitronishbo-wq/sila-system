"""
Auto-generated exceptions for CivilProtection module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('CivilProtection')
CivilProtectionException = _exc.Base
CivilProtectionNotFound = _exc.NotFound
CivilProtectionValidationError = _exc.ValidationError
CivilProtectionUnauthorized = _exc.Unauthorized
CivilProtectionConflict = _exc.Conflict
CivilProtectionInvalidState = _exc.InvalidState
CivilProtectionInvalidStateError = _exc.InvalidStateError