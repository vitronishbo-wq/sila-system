"""Domain exceptions for Statistics module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Statistics')
StatisticsException = exc.Base
StatisticsNotFound = exc.NotFound
StatisticsValidationError = exc.ValidationError
StatisticsInvalidStateError = exc.InvalidStateError
__all__ = ['StatisticsException', 'StatisticsNotFound', 'StatisticsValidationError', 'StatisticsInvalidStateError']