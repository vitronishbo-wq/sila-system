from __future__ import annotations
import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime, Integer, JSON, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class ViagemModel(Base):
    __tablename__ = 'transportes_logistica_viagens'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    linha_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    veiculo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    motorista_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    data_hora_saida: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False, index=True)
    data_hora_chegada_prevista: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    origem: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    destino: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    itinerario: Mapped[list[dict]] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    data_hora_chegada_real: Mapped[datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)
    paradas: Mapped[list[dict] | None] = mapped_column(JSON, nullable=True)
    passageiros_embarcados: Mapped[int | None] = mapped_column(Integer, nullable=True)
    passageiros_desembarcados: Mapped[int | None] = mapped_column(Integer, nullable=True)
    passageiros_transbordo: Mapped[int | None] = mapped_column(Integer, nullable=True)
    carga: Mapped[list[dict] | None] = mapped_column(JSON, nullable=True)
    volume_carga: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    peso_carga: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    valor_frete: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    quilometragem_inicial: Mapped[int | None] = mapped_column(Integer, nullable=True)
    quilometragem_final: Mapped[int | None] = mapped_column(Integer, nullable=True)
    consumo_combustivel: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)