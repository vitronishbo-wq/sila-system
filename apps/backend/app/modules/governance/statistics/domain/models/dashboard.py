from dataclasses import dataclass, field
from datetime import UTC, datetime
from apps.backend.app.modules.governance.statistics.domain.enums import TipoDashboard

@dataclass(slots=True)
class Dashboard:
    nome: str
    tipo: TipoDashboard
    id: int | None = None
    descricao: str | None = None
    configuracoes: dict | None = None
    kpi_ids: list[int] = field(default_factory=list)
    criado_por: int | None = None
    data_criacao: datetime = field(default_factory=lambda: datetime.now(UTC))
    data_atualizacao: datetime = field(default_factory=lambda: datetime.now(UTC))