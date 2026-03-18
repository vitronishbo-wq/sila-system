"""
Auto-generated exceptions for Notifications module
"""
from apps.backend.core.exceptions.factory import ExceptionFactory
_exc = ExceptionFactory.create_module_exceptions('Notifications')
NotificationsException = _exc.Base
NotificationsNotFound = _exc.NotFound
NotificationsValidationError = _exc.ValidationError
NotificationsUnauthorized = _exc.Unauthorized
NotificationsConflict = _exc.Conflict
NotificationsInvalidState = _exc.InvalidState
NotificationsInvalidStateError = _exc.InvalidStateError