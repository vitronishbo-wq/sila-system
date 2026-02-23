from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
import secrets
import uuid


@dataclass(frozen=True)
class Token:
    """Value Object para token JWT"""
    value: str
    expires_at: datetime
    token_type: str  # "access" ou "refresh"
    
    @property
    def is_expired(self) -> bool:
        """Verifica se token expirou"""
        return datetime.now() > self.expires_at
    
    @property
    def time_to_live(self) -> timedelta:
        """Tempo restante de vida do token"""
        if self.is_expired:
            return timedelta(seconds=0)
        return self.expires_at - datetime.now()


@dataclass
class TokenPair:
    """Par de tokens (access + refresh)"""
    access_token: Token
    refresh_token: Token
    token_type: str = "Bearer"
    
    def to_dict(self) -> dict:
        """Converte para dicionário (resposta API)"""
        return {
            "access_token": self.access_token.value,
            "refresh_token": self.refresh_token.value,
            "token_type": self.token_type,
            "expires_in": int(self.access_token.time_to_live.total_seconds())
        }


@dataclass
class RefreshToken:
    """Refresh token armazenado no banco"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = field(default="")
    token_hash: str = field(default="")
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    expires_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(days=30))
    revoked: bool = False
    revoked_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    @classmethod
    def create(cls, user_id: str, ttl_days: int = 30, 
               ip: Optional[str] = None, agent: Optional[str] = None) -> tuple['RefreshToken', str]:
        """Cria novo refresh token e retorna o token original"""
        # Gera token aleatório seguro
        token_value = secrets.token_urlsafe(64)
        
        # Hash do token para armazenamento
        from hashlib import blake2b
        token_hash = blake2b(token_value.encode(), digest_size=32).hexdigest()
        
        expires_at = datetime.now() + timedelta(days=ttl_days)
        
        token = cls(
            id=str(uuid.uuid4()),
            user_id=user_id,
            token_hash=token_hash,
            ip_address=ip,
            user_agent=agent,
            expires_at=expires_at
        )
        
        return token, token_value
    
    @property
    def is_expired(self) -> bool:
        """Verifica se token expirou"""
        return datetime.now() > self.expires_at
    
    @property
    def is_valid(self) -> bool:
        """Verifica se token é válido (não expirado e não revogado)"""
        return not self.is_expired and not self.revoked
    
    def revoke(self):
        """Revoga o token"""
        self.revoked = True
        self.revoked_at = datetime.now()
    
    def verify(self, token_value: str) -> bool:
        """Verifica se o token value corresponde ao hash"""
        from hashlib import blake2b
        token_hash = blake2b(token_value.encode(), digest_size=32).hexdigest()
        return token_hash == self.token_hash
