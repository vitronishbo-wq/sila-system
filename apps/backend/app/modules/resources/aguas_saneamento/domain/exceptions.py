"""Domain exceptions for AguasSaneamento module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('AguasSaneamento')
AguasSaneamentoException = exc.Base
AguasSaneamentoNotFound = exc.NotFound
AguasSaneamentoValidationError = exc.ValidationError
AguasSaneamentoInvalidStateError = exc.InvalidStateError
__all__ = ['AguasSaneamentoException', 'AguasSaneamentoNotFound', 'AguasSaneamentoValidationError', 'AguasSaneamentoInvalidStateError']