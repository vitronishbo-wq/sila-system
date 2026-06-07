from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.app.core.db import Base


class ReclamacaoModel(Base):
    __tablename__ = "dc_reclamacoes"
    __table_args__ = (
        Index("ix_dc_reclamacoes_status_data", "status", "data_abertura"),
        Index("ix_dc_reclamacoes_consumidor_status", "consumidor_id", "status"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    protocolo: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    consumidor_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    estabelecimento_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    produto_servico: Mapped[str] = mapped_column(String(200), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    categoria: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False, default="aberta")
    prioridade: Mapped[str] = mapped_column(String(32), nullable=False, default="media")
    valor_reclamado: Mapped[float | None] = mapped_column(Float, nullable=True)
    data_abertura: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    data_resolucao: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    resolvido: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    descricao_resposta: Mapped[str | None] = mapped_column(Text, nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "protocolo": self.protocolo,
            "consumidor_id": self.consumidor_id,
            "estabelecimento_id": self.estabelecimento_id,
            "produto_servico": self.produto_servico,
            "descricao": self.descricao,
            "categoria": self.categoria,
            "status": self.status,
            "prioridade": self.prioridade,
            "valor_reclamado": self.valor_reclamado,
            "data_abertura": self.data_abertura,
            "data_resolucao": self.data_resolucao,
            "resolvido": self.resolvido,
            "descricao_resposta": self.descricao_resposta,
            "criado_em": self.criado_em,
            "atualizado_em": self.atualizado_em,
        }
