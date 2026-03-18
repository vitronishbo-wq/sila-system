"""Domain exceptions for Ports module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Ports')
PortsException = exc.Base
PortsNotFound = exc.NotFound
PortsValidationError = exc.ValidationError
PortsInvalidStateError = exc.InvalidStateError
__all__ = ['PortsException', 'PortsNotFound', 'PortsValidationError', 'PortsInvalidStateError']