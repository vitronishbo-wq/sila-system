from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Set
from uuid import uuid4

from ..enums.user_status import RoleType
from .permission import Permission, PermissionSet


@dataclass
class Role:
    """Role (função/grupo) do sistema"""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = field(default="")
    description: Optional[str] = None
    role_type: RoleType = RoleType.CUSTOM
    is_system: bool = False  # Roles do sistema não podem ser deletadas
    permissions: Set[Permission] = field(default_factory=set)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.name or len(self.name.strip()) < 2:
            raise ValueError("Nome da role deve ter pelo menos 2 caracteres")
        self.name = self.name.upper().strip()
    
    @property
    def permission_set(self) -> PermissionSet:
        """Retorna PermissionSet para operações"""
        return PermissionSet(self.permissions)
    
    def add_permission(self, permission: Permission):
        """Adiciona permissão à role"""
        self.permissions.add(permission)
        self.updated_at = datetime.now()
    
    def add_permissions(self, *permissions: Permission):
        """Adiciona múltiplas permissões"""
        self.permissions.update(permissions)
        self.updated_at = datetime.now()
    
    def remove_permission(self, permission: Permission):
        """Remove permissão da role"""
        self.permissions.discard(permission)
        self.updated_at = datetime.now()
    
    def has_permission(self, resource: str, action: str) -> bool:
        """Verifica se role tem permissão específica"""
        return self.permission_set.has(resource, action)
    
    def clear_permissions(self):
        """Remove todas as permissões"""
        self.permissions.clear()
        self.updated_at = datetime.now()
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "role_type": self.role_type.value,
            "is_system": self.is_system,
            "permissions": [p.name for p in self.permissions],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if not isinstance(other, Role):
            return False
        return self.id == other.id


@dataclass
class RoleSet:
    """Conjunto de roles com operações"""
    roles: Set[Role] = field(default_factory=set)
    
    def add(self, role: Role):
        """Adiciona role"""
        self.roles.add(role)
    
    def remove(self, role: Role):
        """Remove role"""
        self.roles.discard(role)
    
    @property
    def all_permissions(self) -> PermissionSet:
        """Retorna todas as permissões do conjunto de roles"""
        permissions = set()
        for role in self.roles:
            permissions.update(role.permissions)
        return PermissionSet(permissions)
    
    def has_role(self, role_name: str) -> bool:
        """Verifica se tem uma role específica por nome"""
        return any(r.name == role_name.upper() for r in self.roles)
    
    def has_permission(self, resource: str, action: str) -> bool:
        """Verifica se tem permissão em qualquer role"""
        return self.all_permissions.has(resource, action)
    
    def to_list(self) -> list:
        """Converte para lista de nomes"""
        return [r.name for r in self.roles]
