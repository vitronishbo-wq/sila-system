"""Domain exceptions for UrbanismoHabitacao module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('UrbanismoHabitacao')
UrbanismoHabitacaoException = exc.Base
UrbanismoHabitacaoNotFound = exc.NotFound
UrbanismoHabitacaoValidationError = exc.ValidationError
UrbanismoHabitacaoInvalidStateError = exc.InvalidStateError
__all__ = ['UrbanismoHabitacaoException', 'UrbanismoHabitacaoNotFound', 'UrbanismoHabitacaoValidationError', 'UrbanismoHabitacaoInvalidStateError']