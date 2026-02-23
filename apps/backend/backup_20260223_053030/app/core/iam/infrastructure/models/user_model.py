from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Index, UniqueConstraint, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import BaseModel


class UserModel(BaseModel):
    """Modelo SQLAlchemy para usuários - Alinhado com schema real do BD"""
    __tablename__ = "users"

    # Primary Key (auto-increment INTEGER)
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # UUID for external reference (gen_random_uuid no BD)
    uuid = Column(String(36), unique=True, index=True, nullable=False)
    
    # Autenticação
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    
    # Dados pessoais
    full_name = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    bi_number = Column(String(20), unique=True, nullable=True, index=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    status = Column(String(50), default="ACTIVE", nullable=False, index=True)
    
    # Authorization - Geographic level
    administrative_level = Column(String(20), default="LOCAL", nullable=False)
    
    # Legacy field for compatibility
    level = Column(String(20), nullable=True)
    
    # Geographic assignment - FK to locations (NOT territories!)
    region_id = Column(
        Integer,
        ForeignKey("locations.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    
    # Roles - stored as JSON array
    # Example: ["ADMIN", "USER"] or ["CITIZEN"]
    roles = Column(JSON, default=lambda: [], nullable=False)
    
    # Timestamps
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relacionamentos
    region = relationship("LocationModel", foreign_keys=[region_id])
    
    __table_args__ = (
        Index("idx_users_email_status", "email", "status"),
        Index("idx_users_is_active", "is_active"),
        Index("idx_users_created_at", "created_at"),
    )


class UserRoleModel(BaseModel):
    """Relacionamento usuário-role"""
    __tablename__ = "iam_user_roles"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role_id = Column(String(36), ForeignKey("iam_roles.id", ondelete="CASCADE"), nullable=False, index=True)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    assigned_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relacionamentos
    user = relationship("UserModel", back_populates="roles", foreign_keys=[user_id])
    role = relationship("RoleModel", back_populates="users")
    assigner = relationship("UserModel", foreign_keys=[assigned_by])
    
    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="uq_user_role"),
    )
