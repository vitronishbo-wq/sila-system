"""Edital model for Obras Públicas."""
from sqlalchemy import Column, String, Text, DateTime, Boolean, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from apps.backend.app.core.db import Base


class EditalModel(Base):
    """Modelo SQLAlchemy para Edital (Tender)."""
    __tablename__ = 'obras_publicas_editais'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_edital = Column(String(100), unique=True, nullable=False, index=True)
    titulo = Column(String(500), nullable=False)
    descricao = Column(Text, nullable=True)
    data_publicacao = Column(DateTime, nullable=False, default=func.now(), index=True)
    data_encerramento = Column(DateTime, nullable=True)
    ativo = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
