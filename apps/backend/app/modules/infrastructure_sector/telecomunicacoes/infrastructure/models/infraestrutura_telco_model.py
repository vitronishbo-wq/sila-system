from __future__ import annotations
import uuid
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import Boolean, Date, DateTime, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.domain.db import Base

class InfraestruturaTelcoModel(Base):
    __tablename__ = 'telecom_infraestruturas'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codigo_infra: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    operadora_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    identificador: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    municipio: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    provincia: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    data_implantacao: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 7), nullable=True)
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 7), nullable=True)
    capacidade: Mapped[str | None] = mapped_column(String(120), nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())