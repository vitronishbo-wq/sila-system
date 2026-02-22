from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import BaseModel


class SessionModel(BaseModel):
    """Modelo SQLAlchemy para sessões ativas"""
    __tablename__ = "iam_sessions"

    user_id = Column(String(36), ForeignKey("iam_users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Dados da sessão
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(Text, nullable=True)
    device_id = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    
    # Controle
    is_active = Column(Boolean, default=True, nullable=False)
    last_activity_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    
    # Referência ao refresh token
    refresh_token_id = Column(String(36), ForeignKey("iam_refresh_tokens.id"), nullable=False)
    
    # Relacionamentos
    user = relationship("UserModel", back_populates="sessions")
    refresh_token = relationship("RefreshTokenModel", back_populates="session")
    
    __table_args__ = (
        Index("ix_iam_sessions_user_active", "user_id", "is_active"),
        Index("ix_iam_sessions_expires", "expires_at"),
        Index("ix_iam_sessions_last_activity", "last_activity_at"),
    )


class RefreshTokenModel(BaseModel):
    """Modelo SQLAlchemy para refresh tokens"""
    __tablename__ = "iam_refresh_tokens"

    user_id = Column(String(36), ForeignKey("iam_users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Hash do token (nunca armazenar o token original)
    token_hash = Column(String(128), unique=True, nullable=False, index=True)
    
    # Metadados
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(Text, nullable=True)
    
    # Controle
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    revoked_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relacionamentos
    user = relationship("UserModel", back_populates="refresh_tokens")
    session = relationship("SessionModel", back_populates="refresh_token", uselist=False)
    
    __table_args__ = (
        Index("ix_iam_refresh_tokens_user", "user_id", "expires_at"),
        Index("ix_iam_refresh_tokens_expires", "expires_at"),
        Index("ix_iam_refresh_tokens_revoked", "revoked"),
    )
