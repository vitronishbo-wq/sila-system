from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4


@dataclass
class Session:
    """Sessão de usuário (login ativo)"""
    id: str = field(default_factory=lambda: str(uuid4()))
    user_id: str = field(default="")
    refresh_token_id: str = field(default="")  # Referência ao refresh token
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    device_id: Optional[str] = None
    location: Optional[str] = None
    
    # Controle
    is_active: bool = True
    last_activity_at: datetime = field(default_factory=datetime.now)
    expires_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(hours=24))
    revoked_at: Optional[datetime] = None
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    
    @classmethod
    def create(cls, user_id: str, refresh_token_id: str, ttl_hours: int = 24,
               ip: Optional[str] = None, agent: Optional[str] = None) -> 'Session':
        """Cria nova sessão"""
        expires_at = datetime.now() + timedelta(hours=ttl_hours)
        return cls(
            user_id=user_id,
            refresh_token_id=refresh_token_id,
            ip_address=ip,
            user_agent=agent,
            expires_at=expires_at
        )
    
    @property
    def is_expired(self) -> bool:
        """Verifica se sessão expirou"""
        return datetime.now() > self.expires_at
    
    @property
    def is_valid(self) -> bool:
        """Verifica se sessão é válida"""
        return self.is_active and not self.is_expired and not self.revoked_at
    
    def refresh(self, ttl_hours: int = 24):
        """Renova sessão"""
        self.expires_at = datetime.now() + timedelta(hours=ttl_hours)
        self.last_activity_at = datetime.now()
    
    def update_activity(self):
        """Atualiza timestamp de última atividade"""
        self.last_activity_at = datetime.now()
    
    def revoke(self):
        """Revoga sessão"""
        self.is_active = False
        self.revoked_at = datetime.now()
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "is_active": self.is_active,
            "last_activity_at": self.last_activity_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "created_at": self.created_at.isoformat()
        }
