"""Domain exceptions for SegurancaAlimentar module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('SegurancaAlimentar')
SegurancaAlimentarException = exc.Base
SegurancaAlimentarNotFound = exc.NotFound
SegurancaAlimentarValidationError = exc.ValidationError
SegurancaAlimentarInvalidStateError = exc.InvalidStateError
__all__ = ['SegurancaAlimentarException', 'SegurancaAlimentarNotFound', 'SegurancaAlimentarValidationError', 'SegurancaAlimentarInvalidStateError']