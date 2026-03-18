"""Domain exceptions for PublicBudget module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('PublicBudget')
PublicBudgetException = exc.Base
PublicBudgetNotFound = exc.NotFound
PublicBudgetValidationError = exc.ValidationError
PublicBudgetInvalidStateError = exc.InvalidStateError
__all__ = ['PublicBudgetException', 'PublicBudgetNotFound', 'PublicBudgetValidationError', 'PublicBudgetInvalidStateError']