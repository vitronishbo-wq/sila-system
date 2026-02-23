from sqlalchemy import Column, String, DateTime, Boolean, JSON, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import BaseModel


class AuditLogModel(BaseModel):
    """Modelo SQLAlchemy para logs de auditoria"""
    __tablename__ = "iam_audit_logs"

    # Usuário (pode ser nulo para ações não autenticadas)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    username = Column(String(100), nullable=True)  # Denormalizado para histórico
    
    # Ação
    action = Column(String(50), nullable=False, index=True)  # LOGIN, CREATE, UPDATE, DELETE, etc
    resource = Column(String(50), nullable=False, index=True)  # USER, ROLE, PERMISSION, etc
    resource_id = Column(String(36), nullable=True, index=True)  # ID do recurso afetado
    
    # Detalhes
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(Text, nullable=True)
    details = Column(JSON, nullable=True)  # Dados adicionais estruturados
    
    # Resultado
    success = Column(Boolean, default=True, nullable=False)
    error_message = Column(Text, nullable=True)
    
    # Metadados adicionais
    custom_metadata = Column(JSON, nullable=True)
    
    # Relacionamentos
    user = relationship("UserModel", back_populates="audit_logs")
    
    __table_args__ = (
        Index("ix_iam_audit_logs_user_time", "user_id", "created_at"),
        Index("ix_iam_audit_logs_resource_time", "resource", "resource_id", "created_at"),
        Index("ix_iam_audit_logs_action_time", "action", "created_at"),
        Index("ix_iam_audit_logs_search", "created_at", "user_id", "action"),
    )


class TokenBlacklistModel(BaseModel):
    """Modelo para blacklist de tokens JWT"""
    __tablename__ = "iam_token_blacklist"

    token_jti = Column(String(128), unique=True, nullable=False, index=True)  # JWT ID
    token_type = Column(String(20), nullable=False)  # access, refresh
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    revoked_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    reason = Column(String(255), nullable=True)
    
    __table_args__ = (
        Index("ix_iam_token_blacklist_expires", "expires_at"),
    )
