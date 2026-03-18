"""Domain exceptions for ApoioEmpresarial module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('ApoioEmpresarial')
ApoioEmpresarialException = exc.Base
ApoioEmpresarialNotFound = exc.NotFound
ApoioEmpresarialValidationError = exc.ValidationError
ApoioEmpresarialInvalidStateError = exc.InvalidStateError
__all__ = ['ApoioEmpresarialException', 'ApoioEmpresarialNotFound', 'ApoioEmpresarialValidationError', 'ApoioEmpresarialInvalidStateError']