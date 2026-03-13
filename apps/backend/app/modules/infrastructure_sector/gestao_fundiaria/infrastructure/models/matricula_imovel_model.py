from __future__ import annotations
import uuid
from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from apps.backend.app.core.db import Base

class MatriculaImovelModel(Base):
    __tablename__ = 'gestao_fundiaria_matriculas_imovel'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_matricula: Mapped[str] = mapped_column(String(60), unique=True, nullable=False, index=True)
    imovel_inscricao: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    tipo_registro: Mapped[str] = mapped_column(String(24), nullable=False, index=True)
    cartorio_nome: Mapped[str] = mapped_column(String(255), nullable=False)
    livro: Mapped[str] = mapped_column(String(32), nullable=False)
    folha: Mapped[str] = mapped_column(String(32), nullable=False)
    comarca: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    provincia: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    data_registro: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(24), nullable=False, index=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    proprietario_documento: Mapped[str | None] = mapped_column(String(64), nullable=True)
    data_atualizacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)