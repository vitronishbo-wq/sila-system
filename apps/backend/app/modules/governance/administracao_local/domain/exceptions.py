"""Domain exceptions for AdministracaoLocal module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('AdministracaoLocal')
AdministracaoLocalException = exc.Base
AdministracaoLocalNotFound = exc.NotFound
AdministracaoLocalValidationError = exc.ValidationError
AdministracaoLocalInvalidStateError = exc.InvalidStateError
__all__ = ['AdministracaoLocalException', 'AdministracaoLocalNotFound', 'AdministracaoLocalValidationError', 'AdministracaoLocalInvalidStateError']