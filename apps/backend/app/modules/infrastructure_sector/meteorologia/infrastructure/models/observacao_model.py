from __future__ import annotations
import uuid
from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String, func, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class ObservacaoMeteorologicaModel(Base):
    __tablename__ = 'meteorologia_observacoes'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    estacao_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('meteorologia_estacoes.id', ondelete='CASCADE'), nullable=False, index=True)
    data_observacao: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    temperatura: Mapped[float | None] = mapped_column(nullable=True)
    humidade: Mapped[float | None] = mapped_column(nullable=True)
    pressao: Mapped[float | None] = mapped_column(nullable=True)
    velocidade_vento: Mapped[float | None] = mapped_column(nullable=True)
    direcao_vento: Mapped[float | None] = mapped_column(nullable=True)
    precipitacao: Mapped[float | None] = mapped_column(nullable=True)
    radiacao_solar: Mapped[float | None] = mapped_column(nullable=True)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False, default='SURFACE')
    qualidade_dados: Mapped[str] = mapped_column(String(20), nullable=False, default='VALIDADO')
    has_alerts: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    alertas_json: Mapped[list] = mapped_column('alertas', JSONB, nullable=False, default=list)
    metadata_json: Mapped[dict] = mapped_column('metadata', JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), index=True)
    __table_args__ = (Index('idx_meteorologia_obs_estacao_data', 'estacao_id', 'data_observacao'), Index('idx_meteorologia_obs_alertas_true', 'created_at', postgresql_where=text('has_alerts IS TRUE')))