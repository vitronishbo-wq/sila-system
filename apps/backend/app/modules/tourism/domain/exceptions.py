"""
Auto-generated exceptions for Tourism module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('Tourism')
TourismException = _exc.Base
TourismNotFound = _exc.NotFound
TourismValidationError = _exc.ValidationError
TourismUnauthorized = _exc.Unauthorized
TourismConflict = _exc.Conflict
TourismInvalidState = _exc.InvalidState
TourismInvalidStateError = _exc.InvalidStateError