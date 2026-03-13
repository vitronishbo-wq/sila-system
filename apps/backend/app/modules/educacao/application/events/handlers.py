"""Event handlers for Educação module.

These handlers react to domain events from other modules.
They enable loose coupling between bounded contexts.
"""
from app.domain.events.handlers import EventHandler
from app.domain.observability.enterprise_logging import get_logger
logger = get_logger('modules.educacao.events')

class EducacaoUserLoginHandler(EventHandler):
    """React to user login events in Educação module.
    
    When a user logs in (anywhere in SILA), this handler can:
    - Update last login timestamp for the user's student record
    - Notify about new course information
    - Trigger personalized content recommendations
    - Update access statistics
    
    This is a reactive handler - it doesn't modify the core login logic,
    just adds context-specific behavior.
    """

    async def handle(self, event) -> None:
        """Handle USER_LOGGED_IN event.
        
        Args:
            event: Domain event with user_id in payload
        """
        try:
            user_id = event.payload.get('user_id')
            request_id = event.metadata.get('request_id', 'N/A')
            logger.info('educacao_user_login_handler_processing', extra={'user_id': user_id, 'request_id': request_id})
            logger.debug('educacao_user_login_handler_completed', extra={'user_id': user_id, 'request_id': request_id})
        except Exception as e:
            logger.error('educacao_user_login_handler_failed', extra={'error': str(e), 'event': event.name})
            raise

class EducacaoUserLogoutHandler(EventHandler):
    """React to user logout events in Educação module."""

    async def handle(self, event) -> None:
        """Handle USER_LOGGED_OUT event."""
        user_id = event.payload.get('user_id')
        logger.info('educacao_user_logout_handler_processing', extra={'user_id': user_id})