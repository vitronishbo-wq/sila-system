"""
Auto-generated exceptions for Documents module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('Documents')
DocumentsException = _exc.Base
DocumentsNotFound = _exc.NotFound
DocumentsValidationError = _exc.ValidationError
DocumentsUnauthorized = _exc.Unauthorized
DocumentsConflict = _exc.Conflict
DocumentsInvalidState = _exc.InvalidState
DocumentsInvalidStateError = _exc.InvalidStateError