from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime

from app.core.iam.domain.models.session import Session
from app.core.iam.domain.value_objects.token import RefreshToken


class SessionRepositoryPort(ABC):
    """Interface do repositório de sessões"""
    
    @abstractmethod
    def save_session(self, session: Session) -> Session:
        """Salva uma sessão"""
        pass
    
    @abstractmethod
    def save_refresh_token(self, token: RefreshToken) -> RefreshToken:
        """Salva um refresh token"""
        pass
    
    @abstractmethod
    def get_session_by_id(self, session_id: str) -> Optional[Session]:
        """Busca sessão por ID"""
        pass
    
    @abstractmethod
    def get_refresh_token(self, token_hash: str) -> Optional[RefreshToken]:
        """Busca refresh token por hash"""
        pass
    
    @abstractmethod
    def get_user_sessions(self, user_id: str, active_only: bool = True) -> List[Session]:
        """Lista sessões de um usuário"""
        pass
    
    @abstractmethod
    def get_user_refresh_tokens(self, user_id: str, active_only: bool = True) -> List[RefreshToken]:
        """Lista refresh tokens de um usuário"""
        pass
    
    @abstractmethod
    def revoke_session(self, session_id: str) -> bool:
        """Revoga uma sessão"""
        pass
    
    @abstractmethod
    def revoke_refresh_token(self, token_hash: str) -> bool:
        """Revoga um refresh token"""
        pass
    
    @abstractmethod
    def revoke_all_user_sessions(self, user_id: str, exclude_session_id: Optional[str] = None) -> int:
        """Revoga todas as sessões de um usuário"""
        pass
    
    @abstractmethod
    def revoke_all_user_refresh_tokens(self, user_id: str, exclude_token_id: Optional[str] = None) -> int:
        """Revoga todos os refresh tokens de um usuário"""
        pass
    
    @abstractmethod
    def cleanup_expired(self) -> int:
        """Remove sessões e tokens expirados"""
        pass
    
    @abstractmethod
    def update_session_activity(self, session_id: str) -> bool:
        """Atualiza timestamp de última atividade"""
        pass
