"""Domain exceptions for ServiceRequests module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('ServiceRequests')
ServiceRequestsException = exc.Base
ServiceRequestsNotFound = exc.NotFound
ServiceRequestsValidationError = exc.ValidationError
ServiceRequestsInvalidStateError = exc.InvalidStateError
__all__ = ['ServiceRequestsException', 'ServiceRequestsNotFound', 'ServiceRequestsValidationError', 'ServiceRequestsInvalidStateError']