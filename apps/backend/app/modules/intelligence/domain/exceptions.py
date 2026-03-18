"""
Auto-generated exceptions for Intelligence module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('Intelligence')
IntelligenceException = _exc.Base
IntelligenceNotFound = _exc.NotFound
IntelligenceValidationError = _exc.ValidationError
IntelligenceUnauthorized = _exc.Unauthorized
IntelligenceConflict = _exc.Conflict
IntelligenceInvalidState = _exc.InvalidState
IntelligenceInvalidStateError = _exc.InvalidStateError