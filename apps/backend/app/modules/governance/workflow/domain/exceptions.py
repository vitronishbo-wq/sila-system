"""Domain exceptions for Workflow module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Workflow')
WorkflowException = exc.Base
WorkflowNotFound = exc.NotFound
WorkflowValidationError = exc.ValidationError
WorkflowInvalidStateError = exc.InvalidStateError
__all__ = ['WorkflowException', 'WorkflowNotFound', 'WorkflowValidationError', 'WorkflowInvalidStateError']