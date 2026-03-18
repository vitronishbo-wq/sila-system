"""
Auto-generated exceptions for Logistics module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('Logistics')
LogisticsException = _exc.Base
LogisticsNotFound = _exc.NotFound
LogisticsValidationError = _exc.ValidationError
LogisticsUnauthorized = _exc.Unauthorized
LogisticsConflict = _exc.Conflict
LogisticsInvalidState = _exc.InvalidState
LogisticsInvalidStateError = _exc.InvalidStateError