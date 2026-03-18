"""
Auto-generated exceptions for Procurement module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('Procurement')
ProcurementException = _exc.Base
ProcurementNotFound = _exc.NotFound
ProcurementValidationError = _exc.ValidationError
ProcurementUnauthorized = _exc.Unauthorized
ProcurementConflict = _exc.Conflict
ProcurementInvalidState = _exc.InvalidState
ProcurementInvalidStateError = _exc.InvalidStateError