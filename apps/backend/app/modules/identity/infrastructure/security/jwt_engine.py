from apps.backend.core.auth import JWTHandler

class SovereignJWT(JWTHandler):
    """Wrapper compatível com a interface esperada pelo módulo de identidade."""

    def issue_token(self, subject, roles):
        return self.generate_token(subject, roles=roles)