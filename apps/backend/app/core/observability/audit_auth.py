import logging

logger = logging.getLogger("auth")


class AuthAudit:
    """Audit logging for authentication events"""

    def login_success(self, user):
        """Log successful authentication"""
        logger.info(f"LOGIN_SUCCESS user={user}")

    def login_fail(self, user):
        """Log failed authentication"""
        logger.warning(f"LOGIN_FAIL user={user}")

    def unauthorized(self, ip):
        """Log unauthorized access attempt"""
        logger.warning(f"UNAUTHORIZED_ACCESS ip={ip}")
