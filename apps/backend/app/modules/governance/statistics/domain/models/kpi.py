from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from apps.backend.app.modules.governance.statistics.domain.enums import StatusKPI


@dataclass(slots=True)
class KPI:
    nome: str
    descricao: str
    metrica_id: int
    unidade: str
    id: int | None = None
    valor_alvo: float | None = None
    valor_atual: float | None = None
    valor_anterior: float | None = None
    status: StatusKPI = StatusKPI.ATIVO
    peso: float = 1.0
    limite_inferior: float | None = None
    limite_superior: float | None = None
    data_criacao: datetime = field(default_factory=lambda: datetime.now(UTC))
    data_atualizacao: datetime = field(default_factory=lambda: datetime.now(UTC))

    def calcular_performance(self) -> float:
        if self.valor_alvo in (None, 0) or self.valor_atual is None:
            return 0.0
        return self.valor_atual / self.valor_alvo * 100

    def esta_within_limits(self) -> bool:
        if self.valor_atual is None:
            return True
        if self.limite_inferior is not None and self.valor_atual < self.limite_inferior:
            return False
        if self.limite_superior is not None and self.valor_atual > self.limite_superior:
            return False
        return True

    @property
    def status_cor(self) -> str:
        performance = self.calcular_performance()
        if performance >= 100:
            return "verde"
        if performance >= 80:
            return "amarelo"
        return "vermelho"

    @property
    def performance(self) -> float:
        return self.calcular_performance()

    def atualizar_valor(self, valor: float) -> None:
        self.valor_anterior = self.valor_atual
        self.valor_atual = float(valor)
        self.data_atualizacao = datetime.now(UTC)
