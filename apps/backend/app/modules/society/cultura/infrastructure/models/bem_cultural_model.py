from __future__ import annotations
import uuid
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Boolean, Date, DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.domain.db import Base

class BemCulturalModel(Base):
    __tablename__ = 'cultura_bens_culturais'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    registro_ipat: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    localizacao: Mapped[str] = mapped_column(String(255), nullable=False)
    municipio: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    provincia: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    coordenadas_lat: Mapped[Decimal | None] = mapped_column(Numeric(10, 7), nullable=True)
    coordenadas_long: Mapped[Decimal | None] = mapped_column(Numeric(10, 7), nullable=True)
    status_tombamento: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    tombamento_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True, index=True)
    data_cadastro: Mapped[date] = mapped_column(Date, nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())