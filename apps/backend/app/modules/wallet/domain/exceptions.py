"""
Auto-generated exceptions for Wallet module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('Wallet')
WalletException = _exc.Base
WalletNotFound = _exc.NotFound
WalletValidationError = _exc.ValidationError
WalletUnauthorized = _exc.Unauthorized
WalletConflict = _exc.Conflict
WalletInvalidState = _exc.InvalidState
WalletInvalidStateError = _exc.InvalidStateError