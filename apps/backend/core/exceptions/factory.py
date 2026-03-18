"""
ExceptionFactory - Module exception helpers

Provides a compact API for module-level exceptions:
  exc = ExceptionFactory.create_module_exceptions("Educacao")
  EducacaoException = exc.Base
  EducacaoNotFound = exc.NotFound
  EducacaoValidationError = exc.ValidationError
  EducacaoUnauthorized = exc.Unauthorized
  EducacaoConflict = exc.Conflict
  EducacaoInvalidState = exc.InvalidState
  EducacaoInvalidStateError = exc.InvalidStateError
"""
from types import SimpleNamespace
from typing import Type

from .domain_exception import DomainException
from .module_exception_factory import ModuleExceptionFactory


class ExceptionFactory:
    """Factory for generating module exception bundles."""

    @staticmethod
    def create_module_exceptions(
        module_name: str, base_exception: Type[Exception] | None = None
    ) -> SimpleNamespace:
        """
        Create module exceptions with attribute access.

        Returns:
            SimpleNamespace with Base, NotFound, ValidationError, Unauthorized,
            Conflict, InvalidState, InvalidStateError
        """
        base = base_exception or DomainException
        exc_map = ModuleExceptionFactory.create_exceptions(module_name, base)
        invalid_state = exc_map.get(f"{module_name}InvalidState")
        invalid_state_error = exc_map.get(f"{module_name}InvalidStateError")

        return SimpleNamespace(
            Base=exc_map[f"{module_name}Exception"],
            NotFound=exc_map.get(f"{module_name}NotFound"),
            ValidationError=exc_map.get(f"{module_name}ValidationError"),
            Unauthorized=exc_map.get(f"{module_name}Unauthorized"),
            Conflict=exc_map.get(f"{module_name}Conflict"),
            InvalidState=invalid_state or invalid_state_error,
            InvalidStateError=invalid_state_error or invalid_state,
        )


__all__ = ["ExceptionFactory"]
