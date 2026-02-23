from abc import ABC, abstractmethod
from typing import Optional, List, Tuple

from app.core.iam.domain.models.role import Role


class RoleRepositoryPort(ABC):
    """Interface do repositório de roles"""
    
    @abstractmethod
    def save(self, role: Role) -> Role:
        """Salva ou atualiza uma role"""
        pass
    
    @abstractmethod
    def get_by_id(self, role_id: str) -> Optional[Role]:
        """Busca role por ID"""
        pass
    
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Role]:
        """Busca role por nome"""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100, 
                include_system: bool = True) -> Tuple[List[Role], int]:
        """Lista roles com paginação"""
        pass
    
    @abstractmethod
    def get_by_user(self, user_id: str) -> List[Role]:
        """Busca roles de um usuário"""
        pass
    
    @abstractmethod
    def assign_to_user(self, role_id: str, user_id: str, assigned_by: str) -> bool:
        """Atribui role a um usuário"""
        pass
    
    @abstractmethod
    def remove_from_user(self, role_id: str, user_id: str) -> bool:
        """Remove role de um usuário"""
        pass
    
    @abstractmethod
    def delete(self, role_id: str) -> bool:
        """Remove role (apenas se não for system)"""
        pass
    
    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        """Verifica se role já existe por nome"""
        pass
    
    @abstractmethod
    def get_system_roles(self) -> List[Role]:
        """Retorna roles do sistema"""
        pass
