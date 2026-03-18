"""
Auto-generated exceptions for InfrastructureSector module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('InfrastructureSector')
InfrastructureSectorException = _exc.Base
InfrastructureSectorNotFound = _exc.NotFound
InfrastructureSectorValidationError = _exc.ValidationError
InfrastructureSectorUnauthorized = _exc.Unauthorized
InfrastructureSectorConflict = _exc.Conflict
InfrastructureSectorInvalidState = _exc.InvalidState
InfrastructureSectorInvalidStateError = _exc.InvalidStateError