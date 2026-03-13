"""Event handlers registration for Educação module.

This module imports all handlers and registers them with the global registry.
Called during application startup.
"""
from apps.backend.app.domain.events.registry import HandlerRegistry
from .handlers import EducacaoUserLoginHandler, EducacaoUserLogoutHandler
_user_login_handler = EducacaoUserLoginHandler()
_user_logout_handler = EducacaoUserLogoutHandler()
HandlerRegistry.register('USER_LOGGED_IN', _user_login_handler)
HandlerRegistry.register('USER_LOGGED_OUT', _user_logout_handler)
__all__ = ['EducacaoUserLoginHandler', 'EducacaoUserLogoutHandler']