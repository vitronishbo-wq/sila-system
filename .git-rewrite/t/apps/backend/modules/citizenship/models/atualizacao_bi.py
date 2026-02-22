"""Models for BI update request handling."""

from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from core.db.base_class import Base


class AtualizacaoBI(Base):
    """Model for storing BI update requests."""

    __tablename__ = "citizenship_atualizacao_b_i"
    __table_args__ = {
        "extend_existing": True
    }  # garante que não haja conflito em testes/imports

    id = Column(Integer, primary_key=True, index=True)
    nome_completo = Column(String(200), nullable=False, index=True)
    numero_documento = Column(String(50), nullable=False, unique=True)
    tipo_documento = Column(String(50), nullable=False)
    data_nascimento = Column(DateTime, nullable=False)
    morada = Column(String(500), nullable=False)
    telefone = Column(String(20), nullable=False)
    email = Column(String(200), nullable=False)
    motivo_atualizacao = Column(Text, nullable=False)
    observacoes = Column(Text)
    motivo_cancelamento = Column(Text)
    status = Column(String(50), default="pendente", nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
    dados_adicionais = Column(JSON, nullable=True)  # dados flexíveis adicionais
    user_id = Column(Integer, ForeignKey("citizenship_users.id"), nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow, nullable=False)
    data_atualizacao = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    # user = relationship("User", foreign_keys=[user_id], back_populates="bi_updates")  # Comentado temporariamente
    documents = relationship("AtualizacaoBIDocument", back_populates="bi_update")


class AtualizacaoBIDocument(Base):
    """Model for storing documents related to BI update requests."""

    __tablename__ = "citizenship_atualizacao_b_i_documents"

    id = Column(Integer, primary_key=True, index=True)
    bi_update_id = Column(
        Integer,
        ForeignKey("citizenship_atualizacao_b_i.id"),
        nullable=False,
    )
    document_type = Column(String(100), nullable=False)
    file_path = Column(String(500), nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    verified = Column(Boolean, default=False, nullable=False)
    verification_date = Column(DateTime)
    verification_notes = Column(Text)

    # Relationships
    bi_update = relationship(
        "AtualizacaoBI", foreign_keys=[bi_update_id], back_populates="documents"
    )
