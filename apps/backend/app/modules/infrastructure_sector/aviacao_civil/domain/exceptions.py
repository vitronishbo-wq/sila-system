"""Domain exceptions for AviacaoCivil module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('AviacaoCivil')
AviacaoCivilException = exc.Base
AviacaoCivilNotFound = exc.NotFound
AviacaoCivilValidationError = exc.ValidationError
AviacaoCivilInvalidStateError = exc.InvalidStateError
__all__ = ['AviacaoCivilException', 'AviacaoCivilNotFound', 'AviacaoCivilValidationError', 'AviacaoCivilInvalidStateError']