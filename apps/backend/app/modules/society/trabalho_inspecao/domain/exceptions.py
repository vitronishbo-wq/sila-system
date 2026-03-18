"""Domain exceptions for TrabalhoInspecao module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('TrabalhoInspecao')
TrabalhoInspecaoException = exc.Base
TrabalhoInspecaoNotFound = exc.NotFound
TrabalhoInspecaoValidationError = exc.ValidationError
TrabalhoInspecaoInvalidStateError = exc.InvalidStateError
__all__ = ['TrabalhoInspecaoException', 'TrabalhoInspecaoNotFound', 'TrabalhoInspecaoValidationError', 'TrabalhoInspecaoInvalidStateError']