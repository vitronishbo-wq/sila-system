"""Domain exceptions for AssistenciaSocial module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('AssistenciaSocial')
AssistenciaSocialException = exc.Base
AssistenciaSocialNotFound = exc.NotFound
AssistenciaSocialValidationError = exc.ValidationError
AssistenciaSocialInvalidStateError = exc.InvalidStateError
__all__ = ['AssistenciaSocialException', 'AssistenciaSocialNotFound', 'AssistenciaSocialValidationError', 'AssistenciaSocialInvalidStateError']