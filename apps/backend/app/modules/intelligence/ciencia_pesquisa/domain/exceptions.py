"""Domain exceptions for CienciaPesquisa module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('CienciaPesquisa')
CienciaPesquisaException = exc.Base
CienciaPesquisaNotFound = exc.NotFound
CienciaPesquisaValidationError = exc.ValidationError
CienciaPesquisaInvalidStateError = exc.InvalidStateError
__all__ = ['CienciaPesquisaException', 'CienciaPesquisaNotFound', 'CienciaPesquisaValidationError', 'CienciaPesquisaInvalidStateError']