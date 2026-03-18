"""Domain exceptions for PetroleoGas module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('PetroleoGas')
PetroleoGasException = exc.Base
PetroleoGasNotFound = exc.NotFound
PetroleoGasValidationError = exc.ValidationError
PetroleoGasInvalidStateError = exc.InvalidStateError
__all__ = ['PetroleoGasException', 'PetroleoGasNotFound', 'PetroleoGasValidationError', 'PetroleoGasInvalidStateError']