"""
Auto-generated exceptions for Compliance module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('Compliance')
ComplianceException = _exc.Base
ComplianceNotFound = _exc.NotFound
ComplianceValidationError = _exc.ValidationError
ComplianceUnauthorized = _exc.Unauthorized
ComplianceConflict = _exc.Conflict
ComplianceInvalidState = _exc.InvalidState
ComplianceInvalidStateError = _exc.InvalidStateError