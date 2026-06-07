from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from apps.backend.app.modules.society.juventude.domain.enums import StatusBeneficio, TipoAuxilio


@dataclass
class Auxilio:
    id: UUID
    codigo_auxilio: str
    jovem_id: UUID
    tipo: TipoAuxilio
    data_inicio: date
    status: StatusBeneficio
    data_cadastro: date
    data_fim: date | None = None
    valor_mensal: Decimal | None = None
    observacoes: str | None = None
    ativo: bool = True

    @classmethod
    def conceder(
        cls,
        *,
        codigo_auxilio: str,
        jovem_id: UUID,
        tipo: TipoAuxilio,
        data_inicio: date,
        valor_mensal: Decimal | None = None,
        data_fim: date | None = None,
        observacoes: str | None = None,
    ) -> Auxilio:
        if data_inicio > date.today():
            raise ValueError("Data de inicio do auxilio nao pode estar no futuro")
        if data_fim is not None and data_fim < data_inicio:
            raise ValueError("Data fim deve ser maior ou igual a data de inicio")
        if valor_mensal is not None and valor_mensal < 0:
            raise ValueError("Valor mensal nao pode ser negativo")
        return cls(
            id=uuid4(),
            codigo_auxilio=codigo_auxilio.strip(),
            jovem_id=jovem_id,
            tipo=tipo,
            data_inicio=data_inicio,
            status=StatusBeneficio.ATIVO,
            data_cadastro=date.today(),
            data_fim=data_fim,
            valor_mensal=valor_mensal,
            observacoes=observacoes.strip() if observacoes else None,
            ativo=True,
        )

    def atualizar_status(self, status: StatusBeneficio, observacoes: str | None = None) -> None:
        self.status = status
        self.ativo = status not in {StatusBeneficio.CANCELADO, StatusBeneficio.CONCLUIDO}
        if observacoes is not None:
            self.observacoes = observacoes.strip() or None

    def encerrar(self, observacoes: str | None = None) -> None:
        self.status = StatusBeneficio.CONCLUIDO
        self.ativo = False
        self.data_fim = date.today()
        if observacoes is not None:
            self.observacoes = observacoes.strip() or None
