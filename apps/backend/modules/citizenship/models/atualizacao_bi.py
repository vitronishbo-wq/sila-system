from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Boolean, Integer, String, Text, JSON, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from config.database import Base

if TYPE_CHECKING:
    from modules.identity.models.user import User

class AtualizacaoBI(Base):
    """Modelo para pedidos de atualização de BI."""
    __tablename__ = "citizenship_atualizacao_b_i"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome_completo: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    numero_documento: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    tipo_documento: Mapped[str] = mapped_column(String(50), nullable=False)
    data_nascimento: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    morada: Mapped[str] = mapped_column(String(500), nullable=False)
    telefone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(200), nullable=False, index=True)

    motivo_atualizacao: Mapped[str] = mapped_column(Text, nullable=False)
    observacoes: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="pendente", nullable=False, index=True)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    data_criacao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    data_atualizacao: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user: Mapped["User"] = relationship("User", back_populates="updates_bi")
    documents: Mapped[List["AtualizacaoBIDocument"]] = relationship(back_populates="bi_update", cascade="all, delete-orphan")

class AtualizacaoBIDocument(Base):
    __tablename__ = "citizenship_atualizacao_b_i_documents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    bi_update_id: Mapped[int] = mapped_column(Integer, ForeignKey("citizenship_atualizacao_b_i.id", ondelete="CASCADE"))
    path: Mapped[str] = mapped_column(String(500), nullable=False)
    original_name: Mapped[str] = mapped_column(String(500), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    bi_update: Mapped["AtualizacaoBI"] = relationship(back_populates="documents")