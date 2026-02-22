from sqlalchemy import Column, String, Boolean, Text, UniqueConstraint, Index, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


class RoleModel(BaseModel):
    """Modelo SQLAlchemy para roles"""
    __tablename__ = "iam_roles"

    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    role_type = Column(String(50), nullable=False, default="CUSTOM")  # SYSTEM, CUSTOM, HIERARCHICAL
    is_system = Column(Boolean, default=False, nullable=False)  # Roles do sistema não podem ser deletadas
    
    # Relacionamentos
    users = relationship("UserRoleModel", back_populates="role", cascade="all, delete-orphan")
    permissions = relationship("RolePermissionModel", back_populates="role", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index("ix_iam_roles_name", "name"),
        Index("ix_iam_roles_type", "role_type"),
    )


class RolePermissionModel(BaseModel):
    """Relacionamento role-permissão"""
    __tablename__ = "iam_role_permissions"

    role_id = Column(String(36), ForeignKey("iam_roles.id", ondelete="CASCADE"), nullable=False, index=True)
    permission_id = Column(String(36), ForeignKey("iam_permissions.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Relacionamentos
    role = relationship("RoleModel", back_populates="permissions")
    permission = relationship("PermissionModel", back_populates="roles")
    
    __table_args__ = (
        UniqueConstraint("role_id", "permission_id", name="uq_role_permission"),
    )
