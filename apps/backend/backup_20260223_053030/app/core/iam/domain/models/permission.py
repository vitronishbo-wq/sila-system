from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Set
from uuid import uuid4

from ..enums.user_status import PermissionScope, ActionType, ResourceType


@dataclass
class Permission:
    """Permissão granular do sistema"""
    id: str = field(default_factory=lambda: str(uuid4()))
    resource: ResourceType = field(default=None)
    action: ActionType = field(default=None)
    scope: PermissionScope = PermissionScope.OWN
    description: Optional[str] = None
    is_system: bool = False  # Permissões do sistema não podem ser deletadas
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if not self.resource or not self.action:
            raise ValueError("Resource e action são obrigatórios")
    
    @property
    def name(self) -> str:
        """Nome da permissão no formato resource:action"""
        return f"{self.resource.value}:{self.action.value}"
    
    @classmethod
    def from_string(cls, permission_string: str) -> 'Permission':
        """Cria permissão a partir de string (ex: 'citizen:create')"""
        parts = permission_string.split(':')
        if len(parts) != 2:
            raise ValueError(f"Formato inválido: {permission_string}. Use 'resource:action'")
        
        resource_str, action_str = parts
        try:
            resource = ResourceType(resource_str.upper())
            action = ActionType(action_str.upper())
        except ValueError:
            raise ValueError(f"Resource ou action inválidos: {permission_string}")
        
        return cls(resource=resource, action=action)
    
    def matches(self, resource: ResourceType, action: ActionType) -> bool:
        """Verifica se permissão corresponde ao resource/action"""
        return self.resource == resource and self.action == action
    
    def __hash__(self):
        return hash((self.resource, self.action, self.scope))
    
    def __eq__(self, other):
        if not isinstance(other, Permission):
            return False
        return (self.resource, self.action, self.scope) == (other.resource, other.action, other.scope)


@dataclass
class PermissionSet:
    """Conjunto de permissões com operações úteis"""
    permissions: Set[Permission] = field(default_factory=set)
    
    def add(self, permission: Permission):
        """Adiciona permissão ao conjunto"""
        self.permissions.add(permission)
    
    def remove(self, permission: Permission):
        """Remove permissão do conjunto"""
        self.permissions.discard(permission)
    
    def has(self, resource: ResourceType, action: ActionType, scope: Optional[PermissionScope] = None) -> bool:
        """Verifica se tem permissão específica"""
        for perm in self.permissions:
            if perm.resource == resource and perm.action == action:
                if scope is None or perm.scope == scope or perm.scope == PermissionScope.NATIONAL:
                    return True
        return False
    
    def has_any(self, *permission_strings: str) -> bool:
        """Verifica se tem qualquer uma das permissões (por string)"""
        for perm_str in permission_strings:
            try:
                perm = Permission.from_string(perm_str)
                if self.has(perm.resource, perm.action):
                    return True
            except ValueError:
                continue
        return False
    
    def has_all(self, *permission_strings: str) -> bool:
        """Verifica se tem todas as permissões"""
        for perm_str in permission_strings:
            try:
                perm = Permission.from_string(perm_str)
                if not self.has(perm.resource, perm.action):
                    return False
            except ValueError:
                return False
        return True
    
    def for_resource(self, resource: ResourceType) -> Set[Permission]:
        """Retorna permissões para um recurso específico"""
        return {p for p in self.permissions if p.resource == resource}
    
    def to_list(self) -> list:
        """Converte para lista de strings"""
        return [p.name for p in self.permissions]
    
    def __len__(self):
        return len(self.permissions)
