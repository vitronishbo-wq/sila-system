import jwt
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import uuid
import os


class JWTProvider:
    """Provedor de tokens JWT"""
    
    def __init__(self, 
                 secret_key: Optional[str] = None,
                 algorithm: str = "HS256",
                 access_token_expire_minutes: int = 30,
                 refresh_token_expire_days: int = 7,
                 issuer: str = "sila.gov.ao"):
        self.secret_key = secret_key or os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days
        self.issuer = issuer
    
    def create_access_token(self, user_id: str, roles: list, permissions: list) -> str:
        """
        Gera access token (curta duração)
        """
        now = datetime.utcnow()
        expires = now + timedelta(minutes=self.access_token_expire_minutes)
        
        payload = {
            "sub": user_id,
            "roles": roles,
            "permissions": permissions,
            "iat": now,
            "exp": expires,
            "iss": self.issuer,
            "jti": str(uuid.uuid4()),
            "type": "access"
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, user_id: str) -> str:
        """
        Gera refresh token (longa duração)
        """
        now = datetime.utcnow()
        expires = now + timedelta(days=self.refresh_token_expire_days)
        
        payload = {
            "sub": user_id,
            "iat": now,
            "exp": expires,
            "iss": self.issuer,
            "jti": str(uuid.uuid4()),
            "type": "refresh"
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verifica e decodifica token
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                issuer=self.issuer,
                options={
                    "verify_exp": True,
                    "verify_iss": True
                }
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expirado")
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Token inválido: {str(e)}")
    
    def get_user_id_from_token(self, token: str) -> str:
        """Extrai user_id do token"""
        payload = self.verify_token(token)
        return payload.get("sub")
    
    def refresh_access_token(self, refresh_token: str) -> str:
        """
        Gera novo access token a partir de refresh token
        """
        payload = self.verify_token(refresh_token)
        
        if payload.get("type") != "refresh":
            raise ValueError("Token não é um refresh token válido")
        
        user_id = payload.get("sub")
        # Buscar roles e permissões atuais (será feito pelo service)
        return self.create_access_token(user_id, [], [])
    
    def get_token_jti(self, token: str) -> str:
        """Extrai JTI do token"""
        try:
            # Decodificar sem verificar expiração para pegar JTI
            payload = jwt.decode(
                token,
                options={"verify_signature": False}
            )
            return payload.get("jti")
        except:
            return None


class TokenBlacklist:
    """Gerencia blacklist de tokens JWT"""
    
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self._memory_store = {} if not redis_client else None
    
    def add(self, token_jti: str, expires_at: datetime) -> bool:
        """Adiciona token à blacklist"""
        if self.redis:
            # Redis com expiração automática
            ttl = int((expires_at - datetime.utcnow()).total_seconds())
            if ttl > 0:
                self.redis.setex(f"blacklist:{token_jti}", ttl, "1")
                return True
        else:
            # Fallback em memória
            self._memory_store[token_jti] = expires_at
        return True
    
    def is_blacklisted(self, token_jti: str) -> bool:
        """Verifica se token está na blacklist"""
        if self.redis:
            return self.redis.exists(f"blacklist:{token_jti}") > 0
        else:
            expires = self._memory_store.get(token_jti)
            if expires and expires > datetime.utcnow():
                return True
            if expires:
                del self._memory_store[token_jti]
            return False
    
    def clean_expired(self) -> int:
        """Remove tokens expirados (apenas para memória)"""
        if not self.redis:
            now = datetime.utcnow()
            expired = [jti for jti, exp in self._memory_store.items() if exp <= now]
            for jti in expired:
                del self._memory_store[jti]
            return len(expired)
        return 0
