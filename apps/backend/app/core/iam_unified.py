"""Core IAM - Single source of truth for authentication"""
from typing import Optional, Dict, Any, List
import logging
import os
from functools import lru_cache
from dataclasses import dataclass, field

try:
    from jose import jwt, JWTError
    from passlib.context import CryptContext
except ImportError:
    jwt = None
    JWTError = Exception
    CryptContext = None

logger = logging.getLogger(__name__)

@dataclass
class User:
    """User domain model"""
    id: str
    username: str
    email: str
    permissions: List[str] = field(default_factory=list)
    roles: List[str] = field(default_factory=list)
    tenant_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    is_active: bool = True

class IAMClient:
    """IAM Client unificado"""
    
    def __init__(self):
        self.jwt_secret = os.getenv("JWT_SECRET", "dev-secret-key")
        self.jwt_algorithm = "HS256"
        self.mock_mode = os.getenv("ENVIRONMENT", "development") == "development"
        self._pwd_context = None
    
    @property
    def pwd_context(self):
        if self._pwd_context is None and CryptContext:
            self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return self._pwd_context
    
    async def get_user(self, token: str) -> Optional[User]:
        """Get user from token"""
        if not token:
            return None
        
        try:
            if jwt and JWTError:
                payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
                return User(
                    id=payload.get("sub", "unknown"),
                    username=payload.get("username", "user"),
                    email=payload.get("email", "user@example.com"),
                    permissions=payload.get("permissions", ["read"]),
                    roles=payload.get("roles", ["user"]),
                    tenant_id=payload.get("tenant_id"),
                    is_active=payload.get("is_active", True)
                )
        except Exception as e:
            logger.debug(f"JWT decode failed: {e}")
        
        if self.mock_mode:
            return User(
                id="dev-user", username="dev_user", email="dev@example.com",
                permissions=["*"], roles=["admin"], tenant_id="dev-tenant"
            )
        
        return None
    
    def get_password_hash(self, password: str) -> str:
        if not self.pwd_context:
            raise RuntimeError("CryptContext not initialized")
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain: str, hashed: str) -> bool:
        if not self.pwd_context:
            raise RuntimeError("CryptContext not initialized")
        return self.pwd_context.verify(plain, hashed)

@lru_cache()
def get_iam_client() -> IAMClient:
    return IAMClient()

__all__ = ['IAMClient', 'get_iam_client', 'User']
