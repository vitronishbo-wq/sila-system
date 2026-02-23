from abc import ABC, abstractmethod
from typing import Optional, List, Set, Tuple

from app.core.iam.domain.models.permission import Permission
from app.core.iam.domain.enums.user_status import ResourceType, ActionType


class PermissionRepositoryPort(ABC):
    """Interface do repositório de permissões"""
    
    @abstractmethod
    def save(self, permission: Permission) -> Permission:
        """Salva ou atualiza uma permissão"""
        pass
    
    @abstractmethod
    def get_by_id(self, permission_id: str) -> Optional[Permission]:
        """Busca permissão por ID"""
        pass
    
    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Permission]:
        """Busca permissão por código (resource:action)"""
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> Tuple[List[Permission], int]:
        """Lista permissões com paginação"""
        pass
    
    @abstractmethod
    def get_by_resource(self, resource: ResourceType) -> List[Permission]:
        """Busca permissões por recurso"""
        pass
    
    @abstractmethod
    def get_by_role(self, role_id: str) -> Set[Permission]:
        """Busca permissões de uma role"""
        pass
    
    @abstractmethod
    def get_by_user(self, user_id: str) -> Set[Permission]:
        """Busca todas as permissões de um usuário (via roles + diretas)"""
        pass
    
    @abstractmethod
    def assign_to_role(self, permission_id: str, role_id: str) -> bool:
        """Atribui permissão a uma role"""
        pass
    
    @abstractmethod
    def remove_from_role(self, permission_id: str, role_id: str) -> bool:
        """Remove permissão de uma role"""
        pass
    
    @abstractmethod
    def assign_to_user_direct(self, permission_id: str, user_id: str) -> bool:
        """Atribui permissão diretamente a um usuário"""
        pass
    
    @abstractmethod
    def remove_from_user_direct(self, permission_id: str, user_id: str) -> bool:
        """Remove permissão direta de um usuário"""
        pass
    
    @abstractmethod
    def delete(self, permission_id: str) -> bool:
        """Remove permissão (apenas se não for system)"""
        pass
    
    @abstractmethod
    def exists_by_code(self, code: str) -> bool:
        """Verifica se permissão já existe por código"""
        pass
    
    @abstractmethod
    def get_user_permissions_map(self, user_id: str) -> dict:
        """Retorna mapa de permissões do usuário agrupado por recurso"""
        pass
