from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4


@dataclass
class Colheita:
    id: UUID
    codigo_colheita: str
    codigo_safra: str
    codigo_talhao: str
    quantidade_colhida_ton: float
    perdas_ton: float
    data_colheita: date
    umidade_percentual: float | None = None
    observacoes: str | None = None

    @classmethod
    def registrar(
        cls,
        *,
        codigo_safra: str,
        codigo_talhao: str,
        quantidade_colhida_ton: float,
        perdas_ton: float = 0.0,
        umidade_percentual: float | None = None,
        observacoes: str | None = None,
    ) -> Colheita:
        if quantidade_colhida_ton <= 0:
            raise ValueError("Quantidade colhida deve ser maior que zero")
        if perdas_ton < 0:
            raise ValueError("Perdas nao podem ser negativas")
        if perdas_ton > quantidade_colhida_ton:
            raise ValueError("Perdas nao podem exceder quantidade colhida")
        if umidade_percentual is not None and (not 0 <= umidade_percentual <= 100):
            raise ValueError("Umidade percentual deve estar entre 0 e 100")
        return cls(
            id=uuid4(),
            codigo_colheita="",
            codigo_safra=codigo_safra,
            codigo_talhao=codigo_talhao,
            quantidade_colhida_ton=round(quantidade_colhida_ton, 3),
            perdas_ton=round(perdas_ton, 3),
            data_colheita=date.today(),
            umidade_percentual=round(umidade_percentual, 2)
            if umidade_percentual is not None
            else None,
            observacoes=observacoes,
        )

    @property
    def quantidade_liquida_ton(self) -> float:
        return round(self.quantidade_colhida_ton - self.perdas_ton, 3)
