"""Core Security"""
from typing import Optional, Dict, Any
import logging
import os
from datetime import datetime, timedelta

try:
    from jose import jwt
except ImportError:
    jwt = None

logger = logging.getLogger(__name__)
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    if not jwt:
        raise RuntimeError("PyJWT not installed")
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

class IAMClient:
    """IAM Client wrapper"""
    
    async def get_current_user(self, token: str) -> Optional[Dict[str, Any]]:
        """Get user"""
        from app.core.iam_unified import get_iam_client
        client = get_iam_client()
        user = await client.get_user(token)
        if user:
            return {
                "id": user.id, "username": user.username, "email": user.email,
                "permissions": user.permissions, "roles": user.roles
            }
        return None

def get_password_hash(pwd: str) -> str:
    from passlib.context import CryptContext
    return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(pwd)

def verify_password(plain: str, hashed: str) -> bool:
    from passlib.context import CryptContext
    return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(plain, hashed)

__all__ = [
    'ALGORITHM', 'SECRET_KEY', 'ACCESS_TOKEN_EXPIRE_MINUTES',
    'create_access_token', 'IAMClient', 'get_password_hash', 'verify_password'
]
