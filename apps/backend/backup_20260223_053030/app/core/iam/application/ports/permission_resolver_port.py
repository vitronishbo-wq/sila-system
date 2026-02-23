from abc import ABC, abstractmethod
from datetime import datetime
from typing import Set, List

from app.core.iam.domain.models.user import User
from app.core.iam.domain.models.permission import Permission
from app.core.iam.domain.enums.user_status import ResourceType, ActionType


class PermissionResolverPort(ABC):
    """Interface para resolução de permissões"""
    
    @abstractmethod
    def get_user_permissions(self, user: User) -> Set[Permission]:
        """Obtém todas as permissões de um usuário"""
        pass
    
    @abstractmethod
    def has_permission(self, user: User, resource: ResourceType, 
                      action: ActionType) -> bool:
        """Verifica se usuário tem permissão específica"""
        pass
    
    @abstractmethod
    def has_any_permission(self, user: User, *permission_codes: str) -> bool:
        """Verifica se usuário tem qualquer uma das permissões"""
        pass
    
    @abstractmethod
    def has_all_permissions(self, user: User, *permission_codes: str) -> bool:
        """Verifica se usuário tem todas as permissões"""
        pass
    
    @abstractmethod
    def filter_by_permission(self, users: List[User], 
                           resource: ResourceType,
                           action: ActionType) -> List[User]:
        """Filtra usuários que têm uma permissão"""
        pass
    
    @abstractmethod
    def get_permissions_matrix(self, user: User) -> dict:
        """Retorna matriz de permissões (recurso -> ações)"""
        pass


class TokenBlacklistPort(ABC):
    """Interface para blacklist de tokens"""
    
    @abstractmethod
    def add_to_blacklist(self, token: str, expires_at: datetime) -> bool:
        """Adiciona token à blacklist"""
        pass
    
    @abstractmethod
    def is_blacklisted(self, token: str) -> bool:
        """Verifica se token está na blacklist"""
        pass
    
    @abstractmethod
    def clean_expired(self) -> int:
        """Remove tokens expirados da blacklist"""
        pass
