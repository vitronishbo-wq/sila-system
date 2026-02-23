from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.settings import settings

# Import IAMClient
try:
    from core.security.iam_client import IAMClient
except ImportError:
    # Fallback
    class IAMClient:
        @staticmethod
        def get_current_user(token=None):
            return {"id": 1, "username": "dev", "permissions": ["admin"]}
        
        @staticmethod
        def check_permission(user, perm):
            return True

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

__all__ = [
    "IAMClient",
    "verify_password",
    "get_password_hash",
    "create_access_token",
]

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    # Use ACCESS_TOKEN_EXPIRE_DAYS from settings (backwards compatible)
    days = getattr(settings, 'ACCESS_TOKEN_EXPIRE_DAYS', None)
    if days is None:
        # fallback to older name if present
        days = getattr(settings, 'TOKEN_EXPIRATION_DAYS', 90)
    expire = datetime.utcnow() + timedelta(days=days)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
