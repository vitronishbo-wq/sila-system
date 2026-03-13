"""Obra model for Obras Públicas."""
from sqlalchemy import Column, String, Text, Float, DateTime, Boolean, UUID, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.domain.db import Base


class ObraModel(Base):
    """Modelo SQLAlchemy para Obra (Public Work)."""
    __tablename__ = 'obras_publicas_obras'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_obra = Column(String(100), unique=True, nullable=False, index=True)
    licitacao_id = Column(UUID(as_uuid=True), ForeignKey('obras_publicas_licitacoes.id'), nullable=False, index=True)
    titulo = Column(String(500), nullable=False)
    descricao = Column(Text, nullable=True)
    valor_contrato = Column(Float, nullable=True)
    data_inicio = Column(DateTime, nullable=True)
    data_conclusao_prevista = Column(DateTime, nullable=True)
    data_conclusao_real = Column(DateTime, nullable=True)
    status = Column(String(50), default='NAO_INICIADA', index=True)
    percentual_conclusao = Column(Float, default=0.0)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
