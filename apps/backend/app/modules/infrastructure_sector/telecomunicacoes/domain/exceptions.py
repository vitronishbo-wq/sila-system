"""Domain exceptions for Telecomunicacoes module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Telecomunicacoes')
TelecomunicacoesException = exc.Base
TelecomunicacoesNotFound = exc.NotFound
TelecomunicacoesValidationError = exc.ValidationError
TelecomunicacoesInvalidStateError = exc.InvalidStateError
__all__ = ['TelecomunicacoesException', 'TelecomunicacoesNotFound', 'TelecomunicacoesValidationError', 'TelecomunicacoesInvalidStateError']