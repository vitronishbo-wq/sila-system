from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Text, Index, UniqueConstraint, JSON, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from .base import BaseModel


class UserModel(BaseModel):
    """Modelo SQLAlchemy para usuários"""
    __tablename__ = "iam_users"

    # Autenticação
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Vínculo com cidadão do FUC
    citizen_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    
    # Status
    status = Column(String(50), nullable=False, default="PENDING_VERIFICATION", index=True)
    is_superuser = Column(Boolean, default=False, nullable=False)
    
    # Dados pessoais
    full_name = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    department = Column(String(255), nullable=True)
    position = Column(String(255), nullable=True)
    
    # Controle de segurança
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    last_login_ip = Column(String(50), nullable=True)
    password_changed_at = Column(DateTime(timezone=True), nullable=True)
    password_expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # MFA
    mfa_enabled = Column(Boolean, default=False, nullable=False)
    mfa_secret = Column(String(255), nullable=True)
    mfa_type = Column(String(50), default="NONE", nullable=False)
    
    # Metadados
    custom_metadata = Column(JSON, nullable=True)
    
    # Timestamps
    deleted_at = Column(DateTime(timezone=True), nullable=True)  # Soft delete
    
    # Relacionamentos
    roles = relationship("UserRoleModel", back_populates="user", cascade="all, delete-orphan", foreign_keys="UserRoleModel.user_id")
    sessions = relationship("SessionModel", back_populates="user", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshTokenModel", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLogModel", back_populates="user")
    permissions_direct = relationship("UserPermissionModel", back_populates="user", cascade="all, delete-orphan", foreign_keys="UserPermissionModel.user_id")
    
    __table_args__ = (
        Index("ix_iam_users_status_created", "status", "created_at"),
        Index("ix_iam_users_username_lower", func.lower(username)),
        Index("ix_iam_users_email_lower", func.lower(email)),
        Index("ix_iam_users_citizen_id", "citizen_id"),
        UniqueConstraint("citizen_id", name="uq_iam_users_citizen_id"),
    )


class UserRoleModel(BaseModel):
    """Relacionamento usuário-role"""
    __tablename__ = "iam_user_roles"

    user_id = Column(String(36), ForeignKey("iam_users.id", ondelete="CASCADE"), nullable=False, index=True)
    role_id = Column(String(36), ForeignKey("iam_roles.id", ondelete="CASCADE"), nullable=False, index=True)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    assigned_by = Column(String(36), ForeignKey("iam_users.id"), nullable=True)
    
    # Relacionamentos
    user = relationship("UserModel", back_populates="roles", foreign_keys=[user_id])
    role = relationship("RoleModel", back_populates="users")
    assigner = relationship("UserModel", foreign_keys=[assigned_by])
    
    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="uq_user_role"),
    )
