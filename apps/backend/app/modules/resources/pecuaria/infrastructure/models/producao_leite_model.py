from __future__ import annotations
import uuid
from datetime import date, datetime
from sqlalchemy import Date, DateTime, Float, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.core.db import Base

class ProducaoLeiteModel(Base):
    __tablename__ = 'pecuaria_producao_leite'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    propriedade_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    litros: Mapped[float] = mapped_column(Float, nullable=False)
    data_producao: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)