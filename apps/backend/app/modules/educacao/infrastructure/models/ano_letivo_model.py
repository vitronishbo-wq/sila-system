from __future__ import annotations
import uuid
from sqlalchemy import Boolean, Date, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class AnoLetivoModel(Base):
    __tablename__ = 'educacao_anos_letivos'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ano: Mapped[int] = mapped_column(Integer, nullable=False, unique=True, index=True)
    data_inicio: Mapped[str] = mapped_column(Date, nullable=False)
    data_fim: Mapped[str] = mapped_column(Date, nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)