"""
Auto-generated exceptions for Educacao module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('Educacao')
EducacaoException = _exc.Base
EducacaoNotFound = _exc.NotFound
EducacaoValidationError = _exc.ValidationError
EducacaoUnauthorized = _exc.Unauthorized
EducacaoConflict = _exc.Conflict
EducacaoInvalidState = _exc.InvalidState
EducacaoInvalidStateError = _exc.InvalidStateError