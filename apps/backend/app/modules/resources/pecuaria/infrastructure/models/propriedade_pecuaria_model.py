from __future__ import annotations
import uuid
from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, Float, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.domain.db import Base

class PropriedadePecuariaModel(Base):
    __tablename__ = 'pecuaria_propriedades'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_propriedade: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    pecuarista_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    area_total_ha: Mapped[float] = mapped_column(Float, nullable=False)
    municipio: Mapped[str] = mapped_column(String(120), nullable=False)
    provincia: Mapped[str] = mapped_column(String(120), nullable=False)
    data_cadastro: Mapped[date] = mapped_column(Date, nullable=False, server_default=func.current_date())
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())