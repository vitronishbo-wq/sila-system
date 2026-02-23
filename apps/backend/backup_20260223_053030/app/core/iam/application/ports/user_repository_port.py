from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from datetime import datetime

from app.core.iam.domain.models.user import User
from app.core.iam.domain.value_objects.email import Email


class UserRepositoryPort(ABC):
    """Interface do repositório de usuários"""
    
    @abstractmethod
    def save(self, user: User) -> User:
        """Salva ou atualiza um usuário"""
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Busca usuário por ID"""
        pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """Busca usuário por username"""
        pass
    
    @abstractmethod
    def get_by_email(self, email: Email) -> Optional[User]:
        """Busca usuário por email"""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100, 
                include_inactive: bool = False) -> Tuple[List[User], int]:
        """Lista usuários com paginação"""
        pass
    
    @abstractmethod
    def get_by_role(self, role_id: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Busca usuários por role"""
        pass
    
    @abstractmethod
    def update_last_login(self, user_id: str, ip_address: Optional[str] = None) -> Optional[User]:
        """Atualiza timestamp do último login"""
        pass
    
    @abstractmethod
    def increment_failed_attempts(self, user_id: str) -> Optional[User]:
        """Incrementa contador de tentativas falhas"""
        pass
    
    @abstractmethod
    def reset_failed_attempts(self, user_id: str) -> Optional[User]:
        """Reseta contador de tentativas falhas"""
        pass
    
    @abstractmethod
    def update_password(self, user_id: str, password_hash: str) -> Optional[User]:
        """Atualiza senha do usuário"""
        pass
    
    @abstractmethod
    def delete(self, user_id: str, soft_delete: bool = True) -> bool:
        """Remove usuário (soft delete por padrão)"""
        pass
    
    @abstractmethod
    def exists_by_username(self, username: str) -> bool:
        """Verifica se username já existe"""
        pass
    
    @abstractmethod
    def exists_by_email(self, email: Email) -> bool:
        """Verifica se email já existe"""
        pass
    
    @abstractmethod
    def count_active(self) -> int:
        """Conta usuários ativos"""
        pass
