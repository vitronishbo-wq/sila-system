"""Domain exceptions for Taxpayer module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Taxpayer')
TaxpayerException = exc.Base
TaxpayerNotFound = exc.NotFound
TaxpayerValidationError = exc.ValidationError
TaxpayerInvalidStateError = exc.InvalidStateError
__all__ = ['TaxpayerException', 'TaxpayerNotFound', 'TaxpayerValidationError', 'TaxpayerInvalidStateError']