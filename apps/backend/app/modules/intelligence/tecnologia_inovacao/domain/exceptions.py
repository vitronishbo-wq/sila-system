"""Domain exceptions for TecnologiaInovacao module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('TecnologiaInovacao')
TecnologiaInovacaoException = exc.Base
TecnologiaInovacaoNotFound = exc.NotFound
TecnologiaInovacaoValidationError = exc.ValidationError
TecnologiaInovacaoInvalidStateError = exc.InvalidStateError
__all__ = ['TecnologiaInovacaoException', 'TecnologiaInovacaoNotFound', 'TecnologiaInovacaoValidationError', 'TecnologiaInovacaoInvalidStateError']