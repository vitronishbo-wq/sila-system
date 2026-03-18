"""
Auto-generated exceptions for Industry module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('Industry')
IndustryException = _exc.Base
IndustryNotFound = _exc.NotFound
IndustryValidationError = _exc.ValidationError
IndustryUnauthorized = _exc.Unauthorized
IndustryConflict = _exc.Conflict
IndustryInvalidState = _exc.InvalidState
IndustryInvalidStateError = _exc.InvalidStateError