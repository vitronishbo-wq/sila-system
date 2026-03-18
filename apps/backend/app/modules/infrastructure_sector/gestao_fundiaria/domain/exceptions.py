"""Domain exceptions for GestaoFundiaria module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('GestaoFundiaria')
GestaoFundiariaException = exc.Base
GestaoFundiariaNotFound = exc.NotFound
GestaoFundiariaValidationError = exc.ValidationError
GestaoFundiariaInvalidStateError = exc.InvalidStateError
__all__ = ['GestaoFundiariaException', 'GestaoFundiariaNotFound', 'GestaoFundiariaValidationError', 'GestaoFundiariaInvalidStateError']