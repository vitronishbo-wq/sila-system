"""
Auto-generated exceptions for MigrationService module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('MigrationService')
MigrationServiceException = _exc.Base
MigrationServiceNotFound = _exc.NotFound
MigrationServiceValidationError = _exc.ValidationError
MigrationServiceUnauthorized = _exc.Unauthorized
MigrationServiceConflict = _exc.Conflict
MigrationServiceInvalidState = _exc.InvalidState
MigrationServiceInvalidStateError = _exc.InvalidStateError