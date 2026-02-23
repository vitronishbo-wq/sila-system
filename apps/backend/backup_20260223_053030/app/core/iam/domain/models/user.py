from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Set, List
from uuid import uuid4, UUID

from ..enums.user_status import UserStatus
from ..value_objects.email import Email
from .role import Role, RoleSet


@dataclass
class User:
    """Usuário do sistema"""
    id: str = field(default_factory=lambda: str(uuid4()))
    username: str = field(default="")
    email: Email = field(default=None)
    password_hash: str = field(default="")  # Hash da senha (nunca a senha original)
    citizen_id: Optional[UUID] = None  # ID do cidadão no FUC (se for cidadão)
    status: UserStatus = UserStatus.PENDING_VERIFICATION
    is_superuser: bool = False
    
    # Dados pessoais
    full_name: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    
    # Controle
    roles: Set[Role] = field(default_factory=set)
    failed_login_attempts: int = 0
    last_login_at: Optional[datetime] = None
    last_login_ip: Optional[str] = None
    password_changed_at: Optional[datetime] = None
    password_expires_at: Optional[datetime] = None
    
    # MFA
    mfa_enabled: bool = False
    mfa_secret: Optional[str] = None
    mfa_type: str = "NONE"
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None  # Soft delete
    
    def __post_init__(self):
        if not self.username or len(self.username.strip()) < 3:
            raise ValueError("Username deve ter pelo menos 3 caracteres")
        self.username = self.username.strip().lower()
    
    @property
    def is_active(self) -> bool:
        """Verifica se usuário está ativo"""
        return self.status == UserStatus.ACTIVE
    
    @property
    def is_blocked(self) -> bool:
        """Verifica se usuário está bloqueado"""
        return self.status in [UserStatus.BLOCKED, UserStatus.LOCKED]
    
    @property
    def role_set(self) -> RoleSet:
        """Retorna RoleSet para operações"""
        return RoleSet(self.roles)
    
    def activate(self):
        """Ativa usuário"""
        self.status = UserStatus.ACTIVE
        self.updated_at = datetime.now()
    
    def deactivate(self):
        """Desativa usuário"""
        self.status = UserStatus.INACTIVE
        self.updated_at = datetime.now()
    
    def block(self, reason: Optional[str] = None):
        """Bloqueia usuário"""
        self.status = UserStatus.BLOCKED
        self.updated_at = datetime.now()
    
    def lock(self):
        """Bloqueia por múltiplas tentativas"""
        self.status = UserStatus.LOCKED
        self.updated_at = datetime.now()
    
    def unlock(self):
        """Desbloqueia usuário"""
        self.status = UserStatus.ACTIVE
        self.failed_login_attempts = 0
        self.updated_at = datetime.now()
    
    def add_role(self, role: Role):
        """Adiciona role ao usuário"""
        self.roles.add(role)
        self.updated_at = datetime.now()
    
    def add_roles(self, *roles: Role):
        """Adiciona múltiplas roles"""
        self.roles.update(roles)
        self.updated_at = datetime.now()
    
    def remove_role(self, role: Role):
        """Remove role do usuário"""
        self.roles.discard(role)
        self.updated_at = datetime.now()
    
    def clear_roles(self):
        """Remove todas as roles"""
        self.roles.clear()
        self.updated_at = datetime.now()
    
    def has_role(self, role_name: str) -> bool:
        """Verifica se usuário tem uma role específica"""
        return any(r.name == role_name.upper() for r in self.roles)
    
    def has_permission(self, resource: str, action: str) -> bool:
        """Verifica se usuário tem permissão específica"""
        if self.is_superuser:
            return True
        return self.role_set.has_permission(resource, action)
    
    def has_any_permission(self, *permissions: str) -> bool:
        """Verifica se tem qualquer uma das permissões"""
        if self.is_superuser:
            return True
        return self.role_set.all_permissions.has_any(*permissions)
    
    def has_all_permissions(self, *permissions: str) -> bool:
        """Verifica se tem todas as permissões"""
        if self.is_superuser:
            return True
        return self.role_set.all_permissions.has_all(*permissions)
    
    def record_login(self, ip_address: Optional[str] = None):
        """Regista login bem-sucedido"""
        self.last_login_at = datetime.now()
        self.last_login_ip = ip_address
        self.failed_login_attempts = 0
        self.updated_at = datetime.now()
    
    def record_failed_login(self):
        """Regista tentativa de login falha"""
        self.failed_login_attempts += 1
        self.updated_at = datetime.now()
        
        # Auto-lock após 5 tentativas
        if self.failed_login_attempts >= 5:
            self.lock()
    
    def update_password(self, new_password_hash: str):
        """Atualiza senha do usuário"""
        self.password_hash = new_password_hash
        self.password_changed_at = datetime.now()
        self.failed_login_attempts = 0
        self.updated_at = datetime.now()
        
        # Se estava bloqueado por tentativas, desbloqueia
        if self.status == UserStatus.LOCKED:
            self.status = UserStatus.ACTIVE
    
    def soft_delete(self):
        """Soft delete do usuário"""
        self.deleted_at = datetime.now()
        self.status = UserStatus.INACTIVE
        self.updated_at = datetime.now()
    
    def link_to_citizen(self, citizen_id: UUID):
        """Vincula usuário a um cidadão do FUC"""
        self.citizen_id = citizen_id
        self.updated_at = datetime.now()
    
    def unlink_from_citizen(self):
        """Desvincula usuário do cidadão"""
        self.citizen_id = None
        self.updated_at = datetime.now()
    
    @property
    def is_citizen(self) -> bool:
        """Verifica se é um cidadão (tem vínculo com FUC)"""
        return self.citizen_id is not None
    
    def to_dict(self) -> dict:
        """Converte para dicionário (sem dados sensíveis)"""
        return {
            "id": self.id,
            "username": self.username,
            "email": str(self.email) if self.email else None,
            "citizen_id": str(self.citizen_id) if self.citizen_id else None,
            "full_name": self.full_name,
            "status": self.status.value,
            "is_superuser": self.is_superuser,
            "is_citizen": self.is_citizen,
            "mfa_enabled": self.mfa_enabled,
            "roles": [r.name for r in self.roles],
            "permissions": self.role_set.all_permissions.to_list(),
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id
