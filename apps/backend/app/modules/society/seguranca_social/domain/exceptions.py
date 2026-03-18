"""Domain exceptions for SegurancaSocial module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('SegurancaSocial')
SegurancaSocialException = exc.Base
SegurancaSocialNotFound = exc.NotFound
SegurancaSocialValidationError = exc.ValidationError
SegurancaSocialInvalidStateError = exc.InvalidStateError
__all__ = ['SegurancaSocialException', 'SegurancaSocialNotFound', 'SegurancaSocialValidationError', 'SegurancaSocialInvalidStateError']