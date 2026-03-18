"""
Auto-generated exceptions for Audit module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('Audit')
AuditException = _exc.Base
AuditNotFound = _exc.NotFound
AuditValidationError = _exc.ValidationError
AuditUnauthorized = _exc.Unauthorized
AuditConflict = _exc.Conflict
AuditInvalidState = _exc.InvalidState
AuditInvalidStateError = _exc.InvalidStateError