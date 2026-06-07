from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import (
    StatusParcelamento,
    TipoParcelamento,
)


@dataclass
class Parcelamento:
    id: UUID
    codigo_parcelamento: str
    nome: str
    tipo: TipoParcelamento
    status: StatusParcelamento
    plano_diretor_id: UUID
    zoneamento_id: UUID
    provincia: str
    area_total: Decimal
    quantidade_unidades_prevista: int
    municipio: str | None = None
    area_publica_prevista: Decimal | None = None
    area_sistema_viario_prevista: Decimal | None = None
    quantidade_unidades_resultante: int | None = None
    data_cadastro: date = field(default_factory=date.today)
    data_atualizacao: date | None = None
    observacoes: str | None = None

    @classmethod
    def criar(
        cls,
        *,
        codigo_parcelamento: str,
        nome: str,
        tipo: TipoParcelamento,
        plano_diretor_id: UUID,
        zoneamento_id: UUID,
        provincia: str,
        area_total: Decimal,
        quantidade_unidades_prevista: int,
        municipio: str | None = None,
        area_publica_prevista: Decimal | None = None,
        area_sistema_viario_prevista: Decimal | None = None,
    ) -> Parcelamento:
        if not codigo_parcelamento.strip():
            raise ValueError("Codigo do parcelamento e obrigatorio")
        if not nome.strip():
            raise ValueError("Nome do parcelamento e obrigatorio")
        if not provincia.strip():
            raise ValueError("Provincia e obrigatoria")
        if area_total <= 0:
            raise ValueError("Area total deve ser maior que zero")
        if quantidade_unidades_prevista <= 0:
            raise ValueError("Quantidade de unidades prevista deve ser maior que zero")
        return cls(
            id=uuid4(),
            codigo_parcelamento=codigo_parcelamento.strip(),
            nome=nome.strip(),
            tipo=tipo,
            status=StatusParcelamento.ELABORACAO,
            plano_diretor_id=plano_diretor_id,
            zoneamento_id=zoneamento_id,
            provincia=provincia.strip(),
            area_total=area_total,
            quantidade_unidades_prevista=quantidade_unidades_prevista,
            municipio=municipio.strip() if municipio else None,
            area_publica_prevista=area_publica_prevista,
            area_sistema_viario_prevista=area_sistema_viario_prevista,
        )

    def iniciar_analise(self) -> None:
        if self.status != StatusParcelamento.ELABORACAO:
            raise ValueError("Parcelamento precisa estar em elaboracao")
        self.status = StatusParcelamento.EM_ANALISE
        self.data_atualizacao = date.today()

    def aprovar(self) -> None:
        if self.status != StatusParcelamento.EM_ANALISE:
            raise ValueError("Parcelamento precisa estar em analise")
        self.status = StatusParcelamento.APROVADO
        self.data_atualizacao = date.today()

    def iniciar_execucao(self) -> None:
        if self.status != StatusParcelamento.APROVADO:
            raise ValueError("Parcelamento precisa estar aprovado")
        self.status = StatusParcelamento.EM_EXECUCAO
        self.data_atualizacao = date.today()

    def concluir(self, *, quantidade_unidades_resultante: int) -> None:
        if self.status != StatusParcelamento.EM_EXECUCAO:
            raise ValueError("Parcelamento precisa estar em execucao")
        if quantidade_unidades_resultante <= 0:
            raise ValueError("Quantidade de unidades resultante deve ser maior que zero")
        self.status = StatusParcelamento.CONCLUIDO
        self.quantidade_unidades_resultante = quantidade_unidades_resultante
        self.data_atualizacao = date.today()

    def cancelar(self, *, motivo: str) -> None:
        if self.status in {StatusParcelamento.CONCLUIDO, StatusParcelamento.CANCELADO}:
            raise ValueError("Parcelamento nao pode ser cancelado neste status")
        if not motivo.strip():
            raise ValueError("Motivo do cancelamento e obrigatorio")
        self.status = StatusParcelamento.CANCELADO
        self.observacoes = motivo.strip()
        self.data_atualizacao = date.today()
