"""
Auto-generated exceptions for Energy module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('Energy')
EnergyException = _exc.Base
EnergyNotFound = _exc.NotFound
EnergyValidationError = _exc.ValidationError
EnergyUnauthorized = _exc.Unauthorized
EnergyConflict = _exc.Conflict
EnergyInvalidState = _exc.InvalidState
EnergyInvalidStateError = _exc.InvalidStateError