"""
Auto-generated exceptions for Society module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('Society')
SocietyException = _exc.Base
SocietyNotFound = _exc.NotFound
SocietyValidationError = _exc.ValidationError
SocietyUnauthorized = _exc.Unauthorized
SocietyConflict = _exc.Conflict
SocietyInvalidState = _exc.InvalidState
SocietyInvalidStateError = _exc.InvalidStateError