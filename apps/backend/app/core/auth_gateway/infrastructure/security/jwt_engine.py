from jose import jwt
from datetime import datetime, timedelta

SECRET = "SILA_SOVEREIGN_STATE_SECRET_KEY"
ALGO = "HS256"


class JWTEngine:
    """High-performance JWT generation and validation"""

    def generate(self, subject, roles):
        """Generate JWT token with roles and 12-hour expiration"""
        payload = {
            "sub": subject,
            "roles": roles,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=12)
        }
        return jwt.encode(payload, SECRET, algorithm=ALGO)

    def verify(self, token):
        """Verify JWT token and extract payload"""
        return jwt.decode(token, SECRET, algorithms=[ALGO])
