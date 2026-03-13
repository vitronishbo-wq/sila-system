from __future__ import annotations
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from app.modules.governance.statistics.domain.enums import FonteDados, Periodicidade, TipoMetrica

@dataclass(slots=True)
class Metrica:
    nome: str
    descricao: str
    tipo: TipoMetrica
    unidade: str
    fonte_dados: FonteDados
    periodicidade: Periodicidade
    id: int | None = None
    formula: str | None = None
    parametros: dict[str, Any] | None = None
    valor_atual: float | None = None
    valor_anterior: float | None = None
    variacao_percentual: float | None = None
    ativo: bool = True
    data_criacao: datetime = field(default_factory=lambda: datetime.now(UTC))
    data_atualizacao: datetime = field(default_factory=lambda: datetime.now(UTC))
    ultima_atualizacao: datetime | None = None

    def calcular_variacao(self) -> float | None:
        if self.valor_anterior in (None, 0) or self.valor_atual is None:
            self.variacao_percentual = None
            return self.variacao_percentual
        self.variacao_percentual = (self.valor_atual - self.valor_anterior) / self.valor_anterior * 100
        return self.variacao_percentual

    def atualizar_valor(self, novo_valor: float) -> None:
        self.valor_anterior = self.valor_atual
        self.valor_atual = float(novo_valor)
        self.ultima_atualizacao = datetime.now(UTC)
        self.data_atualizacao = datetime.now(UTC)
        self.calcular_variacao()

    @property
    def tendencia(self) -> str:
        if self.variacao_percentual is None:
            return 'estavel'
        if self.variacao_percentual > 0:
            return 'crescente'
        if self.variacao_percentual < 0:
            return 'decrescente'
        return 'estavel'