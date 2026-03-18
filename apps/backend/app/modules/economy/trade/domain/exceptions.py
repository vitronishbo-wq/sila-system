"""Domain exceptions for Trade module"""
from apps.backend.core.exceptions.factory import ExceptionFactory
exc = ExceptionFactory.create_module_exceptions('Trade')
TradeException = exc.Base
TradeNotFound = exc.NotFound
TradeValidationError = exc.ValidationError
TradeInvalidStateError = exc.InvalidStateError
__all__ = ['TradeException', 'TradeNotFound', 'TradeValidationError', 'TradeInvalidStateError']