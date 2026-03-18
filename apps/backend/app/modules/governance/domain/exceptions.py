"""
Auto-generated exceptions for Governance module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('Governance')
GovernanceException = _exc.Base
GovernanceNotFound = _exc.NotFound
GovernanceValidationError = _exc.ValidationError
GovernanceUnauthorized = _exc.Unauthorized
GovernanceConflict = _exc.Conflict
GovernanceInvalidState = _exc.InvalidState
GovernanceInvalidStateError = _exc.InvalidStateError