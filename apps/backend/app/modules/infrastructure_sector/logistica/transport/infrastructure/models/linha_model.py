"""Linha model for Transport."""
from sqlalchemy import Column, String, Integer, DateTime, Boolean, UUID, ForeignKey
from sqlalchemy.sql import func
import uuid
from app.domain.db import Base


class LinhaModel(Base):
    """Modelo SQLAlchemy para Linha."""
    __tablename__ = 'transporte_linhas'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_linha = Column(String(100), unique=True, nullable=False, index=True)
    frota_id = Column(UUID(as_uuid=True), ForeignKey('transporte_frota.id'), nullable=False, index=True)
    origem = Column(String(255), nullable=False)
    destino = Column(String(255), nullable=False)
    status = Column(String(50), default='ATIVA', index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
