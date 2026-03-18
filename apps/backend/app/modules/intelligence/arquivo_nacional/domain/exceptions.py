"""Domain exceptions for ArquivoNacional module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('ArquivoNacional')
ArquivoNacionalException = exc.Base
ArquivoNacionalNotFound = exc.NotFound
ArquivoNacionalValidationError = exc.ValidationError
ArquivoNacionalInvalidStateError = exc.InvalidStateError
__all__ = ['ArquivoNacionalException', 'ArquivoNacionalNotFound', 'ArquivoNacionalValidationError', 'ArquivoNacionalInvalidStateError']