"""
Auto-generated exceptions for Infrastructure module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('Infrastructure')
InfrastructureException = _exc.Base
InfrastructureNotFound = _exc.NotFound
InfrastructureValidationError = _exc.ValidationError
InfrastructureUnauthorized = _exc.Unauthorized
InfrastructureConflict = _exc.Conflict
InfrastructureInvalidState = _exc.InvalidState
InfrastructureInvalidStateError = _exc.InvalidStateError