from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4


@dataclass
class MedicaoObra:
    id: UUID
    periodo_referencia: str
    valor_medido: Decimal
    percentual_executado: Decimal
    data_medicao: date
    fiscal_id: UUID
    documentos: list[str] = field(default_factory=list)
    observacoes: str | None = None

    @classmethod
    def registrar(
        cls,
        *,
        periodo_referencia: str,
        valor_medido: Decimal,
        percentual_executado: Decimal,
        fiscal_id: UUID,
        data_medicao: date | None = None,
        documentos: list[str] | None = None,
        observacoes: str | None = None,
    ) -> MedicaoObra:
        if not periodo_referencia.strip():
            raise ValueError("Periodo de referencia da medicao e obrigatorio")
        if valor_medido <= Decimal("0"):
            raise ValueError("Valor medido deve ser maior que zero")
        if percentual_executado < Decimal("0") or percentual_executado > Decimal("100"):
            raise ValueError("Percentual executado deve estar entre 0 e 100")
        return cls(
            id=uuid4(),
            periodo_referencia=periodo_referencia.strip(),
            valor_medido=valor_medido.quantize(Decimal("0.01")),
            percentual_executado=percentual_executado.quantize(Decimal("0.01")),
            data_medicao=data_medicao or date.today(),
            fiscal_id=fiscal_id,
            documentos=list(documentos or []),
            observacoes=observacoes.strip() if observacoes else None,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "periodo_referencia": self.periodo_referencia,
            "valor_medido": str(self.valor_medido),
            "percentual_executado": str(self.percentual_executado),
            "data_medicao": self.data_medicao.isoformat(),
            "fiscal_id": str(self.fiscal_id),
            "documentos": self.documentos,
            "observacoes": self.observacoes,
        }
