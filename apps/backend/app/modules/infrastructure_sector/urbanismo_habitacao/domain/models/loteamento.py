from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import (
    StatusLoteamento,
    TipoLoteamento,
)


@dataclass
class Loteamento:
    id: UUID
    codigo_loteamento: str
    nome: str
    tipo: TipoLoteamento
    status: StatusLoteamento
    parcelamento_id: UUID
    plano_diretor_id: UUID
    zoneamento_id: UUID
    provincia: str
    area_total: Decimal
    quantidade_lotes_prevista: int
    municipio: str | None = None
    quantidade_lotes_implantada: int = 0
    area_lotes: Decimal | None = None
    area_verde: Decimal | None = None
    area_institucional: Decimal | None = None
    data_inicio_prevista: date | None = None
    data_fim_prevista: date | None = None
    data_inicio_real: date | None = None
    data_fim_real: date | None = None
    data_cadastro: date = field(default_factory=date.today)
    data_atualizacao: date | None = None
    observacoes: str | None = None

    @classmethod
    def criar(
        cls,
        *,
        codigo_loteamento: str,
        nome: str,
        tipo: TipoLoteamento,
        parcelamento_id: UUID,
        plano_diretor_id: UUID,
        zoneamento_id: UUID,
        provincia: str,
        area_total: Decimal,
        quantidade_lotes_prevista: int,
        municipio: str | None = None,
        area_lotes: Decimal | None = None,
        area_verde: Decimal | None = None,
        area_institucional: Decimal | None = None,
        data_inicio_prevista: date | None = None,
        data_fim_prevista: date | None = None,
    ) -> Loteamento:
        if not codigo_loteamento.strip():
            raise ValueError("Codigo do loteamento e obrigatorio")
        if not nome.strip():
            raise ValueError("Nome do loteamento e obrigatorio")
        if not provincia.strip():
            raise ValueError("Provincia e obrigatoria")
        if area_total <= 0:
            raise ValueError("Area total deve ser maior que zero")
        if quantidade_lotes_prevista <= 0:
            raise ValueError("Quantidade de lotes prevista deve ser maior que zero")
        if (
            data_inicio_prevista
            and data_fim_prevista
            and (data_fim_prevista <= data_inicio_prevista)
        ):
            raise ValueError("Data fim prevista deve ser maior que data inicio prevista")
        return cls(
            id=uuid4(),
            codigo_loteamento=codigo_loteamento.strip(),
            nome=nome.strip(),
            tipo=tipo,
            status=StatusLoteamento.PROPOSTO,
            parcelamento_id=parcelamento_id,
            plano_diretor_id=plano_diretor_id,
            zoneamento_id=zoneamento_id,
            provincia=provincia.strip(),
            area_total=area_total,
            quantidade_lotes_prevista=quantidade_lotes_prevista,
            municipio=municipio.strip() if municipio else None,
            area_lotes=area_lotes,
            area_verde=area_verde,
            area_institucional=area_institucional,
            data_inicio_prevista=data_inicio_prevista,
            data_fim_prevista=data_fim_prevista,
        )

    def aprovar(self) -> None:
        if self.status != StatusLoteamento.PROPOSTO:
            raise ValueError("Loteamento precisa estar proposto")
        self.status = StatusLoteamento.APROVADO
        self.data_atualizacao = date.today()

    def iniciar_implantacao(self, *, data_inicio_real: date) -> None:
        if self.status != StatusLoteamento.APROVADO:
            raise ValueError("Loteamento precisa estar aprovado")
        self.status = StatusLoteamento.EM_IMPLANTACAO
        self.data_inicio_real = data_inicio_real
        self.data_atualizacao = date.today()

    def registrar_implantacao(self, *, quantidade_lotes_implantada: int) -> None:
        if self.status != StatusLoteamento.EM_IMPLANTACAO:
            raise ValueError("Loteamento precisa estar em implantacao")
        if quantidade_lotes_implantada <= 0:
            raise ValueError("Quantidade implantada deve ser maior que zero")
        if quantidade_lotes_implantada > self.quantidade_lotes_prevista:
            raise ValueError("Quantidade implantada nao pode exceder a prevista")
        self.quantidade_lotes_implantada = quantidade_lotes_implantada
        self.data_atualizacao = date.today()

    def concluir(self, *, data_fim_real: date) -> None:
        if self.status != StatusLoteamento.EM_IMPLANTACAO:
            raise ValueError("Loteamento precisa estar em implantacao")
        if self.quantidade_lotes_implantada <= 0:
            raise ValueError("Quantidade implantada deve ser maior que zero")
        if self.data_inicio_real and data_fim_real <= self.data_inicio_real:
            raise ValueError("Data fim real deve ser maior que data inicio real")
        self.status = StatusLoteamento.CONCLUIDO
        self.data_fim_real = data_fim_real
        self.data_atualizacao = date.today()

    def suspender(self, *, motivo: str) -> None:
        if self.status != StatusLoteamento.EM_IMPLANTACAO:
            raise ValueError("Apenas loteamento em implantacao pode ser suspenso")
        if not motivo.strip():
            raise ValueError("Motivo da suspensao e obrigatorio")
        self.status = StatusLoteamento.SUSPENSO
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()

    def retomar(self) -> None:
        if self.status != StatusLoteamento.SUSPENSO:
            raise ValueError("Apenas loteamento suspenso pode ser retomado")
        self.status = StatusLoteamento.EM_IMPLANTACAO
        self.data_atualizacao = date.today()

    def cancelar(self, *, motivo: str) -> None:
        if self.status in {StatusLoteamento.CONCLUIDO, StatusLoteamento.CANCELADO}:
            raise ValueError("Loteamento nao pode ser cancelado neste status")
        if not motivo.strip():
            raise ValueError("Motivo do cancelamento e obrigatorio")
        self.status = StatusLoteamento.CANCELADO
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()
