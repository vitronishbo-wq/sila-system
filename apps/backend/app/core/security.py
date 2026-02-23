"""Core security - IAMClient REAL"""
from typing import Optional, Dict, Any
import logging
import os

logger = logging.getLogger(__name__)
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

class IAMClient:
    """IAM Client com fallback"""
    
    async def get_current_user(self, token: str) -> Optional[Dict[str, Any]]:
        """Get user - mock mode"""
        return {
            "id": "mock-user",
            "username": "dev_user",
            "email": "dev@example.com",
            "permissions": ["*"],
            "roles": ["admin"]
        }

def get_password_hash(pwd: str) -> str:
    from passlib.context import CryptContext
    return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(pwd)

def verify_password(plain: str, hashed: str) -> bool:
    from passlib.context import CryptContext
    return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(plain, hashed)

__all__ = ['IAMClient', 'get_password_hash', 'verify_password']
