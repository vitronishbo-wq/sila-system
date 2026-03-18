"""
Auto-generated exceptions for Saude module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('Saude')
SaudeException = _exc.Base
SaudeNotFound = _exc.NotFound
SaudeValidationError = _exc.ValidationError
SaudeUnauthorized = _exc.Unauthorized
SaudeConflict = _exc.Conflict
SaudeInvalidState = _exc.InvalidState
SaudeInvalidStateError = _exc.InvalidStateError