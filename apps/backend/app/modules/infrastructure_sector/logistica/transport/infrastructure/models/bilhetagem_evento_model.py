"""Bilhetagem Evento model for Transport."""
from sqlalchemy import Column, String, DateTime, UUID, ForeignKey
from sqlalchemy.sql import func
import uuid
from app.core.db import Base


class BilhetagemEventoModel(Base):
    """Modelo SQLAlchemy para Evento de Bilhetagem."""
    __tablename__ = 'transporte_bilhetagem_eventos'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_evento = Column(String(100), unique=True, nullable=False, index=True)
    viagem_id = Column(UUID(as_uuid=True), ForeignKey('transporte_viagens.id'), nullable=False, index=True)
    tipo_evento = Column(String(50), nullable=False, index=True)
    data_evento = Column(DateTime, nullable=False, default=func.now())
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
