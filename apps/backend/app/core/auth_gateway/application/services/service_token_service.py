import secrets


class ServiceTokenService:
    """Service-to-service authentication via cryptographic tokens"""

    registry = {}

    def issue(self, service):
        """Issue cryptographic token for service"""
        token = secrets.token_hex(64)
        self.registry[token] = service
        return token

    def verify(self, token):
        """Verify service token"""
        return self.registry.get(token)
