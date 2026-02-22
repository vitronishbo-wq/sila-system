from sqlalchemy import Column, String, Text, UniqueConstraint, Index, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import BaseModel


class PermissionModel(BaseModel):
    """Modelo SQLAlchemy para permissões"""
    __tablename__ = "iam_permissions"

    # Código único no formato: resource:action
    code = Column(String(100), unique=True, nullable=False, index=True)
    
    # Componentes da permissão
    module = Column(String(50), nullable=False, index=True)
    resource = Column(String(50), nullable=False, index=True)
    action = Column(String(50), nullable=False, index=True)
    scope = Column(String(50), nullable=False, default="OWN")  # OWN, UNIT, PROVINCE, NATIONAL
    
    description = Column(Text, nullable=True)
    is_system = Column(Boolean, default=False, nullable=False)  # Permissões do sistema não podem ser deletadas
    
    # Metadados
    custom_metadata = Column(JSON, nullable=True)
    
    # Relacionamentos
    roles = relationship("RolePermissionModel", back_populates="permission", cascade="all, delete-orphan")
    users_direct = relationship("UserPermissionModel", back_populates="permission", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("ix_iam_permissions_module_resource", "module", "resource"),
        Index("ix_iam_permissions_resource_action", "resource", "action"),
        UniqueConstraint("module", "resource", "action", name="uq_permission_components"),
    )


class UserPermissionModel(BaseModel):
    """Permissões diretas atribuídas a usuários (override)"""
    __tablename__ = "iam_user_permissions"

    user_id = Column(String(36), ForeignKey("iam_users.id", ondelete="CASCADE"), nullable=False, index=True)
    permission_id = Column(String(36), ForeignKey("iam_permissions.id", ondelete="CASCADE"), nullable=False, index=True)
    granted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    granted_by = Column(String(36), ForeignKey("iam_users.id"), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)  # Permissão temporária
    
    # Relacionamentos
    user = relationship("UserModel", back_populates="permissions_direct", foreign_keys=[user_id])
    permission = relationship("PermissionModel", back_populates="users_direct")
    granter = relationship("UserModel", foreign_keys=[granted_by])
    
    __table_args__ = (
        UniqueConstraint("user_id", "permission_id", name="uq_user_permission"),
        Index("ix_iam_user_permissions_expires", "expires_at"),
    )
