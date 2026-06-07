from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.modules.resources.agricultura.domain.enums import StatusCredito


@dataclass
class CreditoRural:
    id: UUID
    codigo_credito: str
    codigo_produtor: str
    finalidade: str
    valor_solicitado: float
    valor_aprovado: float | None
    status: StatusCredito
    data_solicitacao: date
    data_aprovacao: date | None = None
    data_desembolso: date | None = None

    @classmethod
    def solicitar(
        cls, *, codigo_produtor: str, finalidade: str, valor_solicitado: float
    ) -> CreditoRural:
        if valor_solicitado <= 0:
            raise ValueError("Valor solicitado deve ser maior que zero")
        return cls(
            id=uuid4(),
            codigo_credito="",
            codigo_produtor=codigo_produtor,
            finalidade=finalidade,
            valor_solicitado=round(valor_solicitado, 2),
            valor_aprovado=None,
            status=StatusCredito.SOLICITADO,
            data_solicitacao=date.today(),
        )

    def aprovar(self, valor_aprovado: float) -> None:
        if self.status != StatusCredito.SOLICITADO:
            raise ValueError("Apenas credito solicitado pode ser aprovado")
        if valor_aprovado <= 0:
            raise ValueError("Valor aprovado deve ser maior que zero")
        if valor_aprovado > self.valor_solicitado:
            raise ValueError("Valor aprovado nao pode exceder valor solicitado")
        self.valor_aprovado = round(valor_aprovado, 2)
        self.status = StatusCredito.APROVADO
        self.data_aprovacao = date.today()

    def desembolsar(self) -> None:
        if self.status != StatusCredito.APROVADO:
            raise ValueError("Apenas credito aprovado pode ser desembolsado")
        self.status = StatusCredito.DESEMBOLSADO
        self.data_desembolso = date.today()
