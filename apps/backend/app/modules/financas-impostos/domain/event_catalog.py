from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4


@dataclass
class NifEmitido:
    event_type: str = "nif_emitido"
    version: int = 1
    nif: str = ""
    cidadao_id: UUID | None = None
    empresa_id: UUID | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class DeclaracaoSubmetida:
    event_type: str = "declaracao_submetida"
    version: int = 1
    declaracao_id: UUID | None = None
    nif: str = ""
    tipo_declaracao: str = ""
    periodo: str = ""
    valor: Decimal = Decimal("0")
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class PagamentoTributarioRecebido:
    event_type: str = "pagamento_tributario_recebido"
    version: int = 1
    pagamento_id: UUID | None = None
    nif: str = ""
    valor: Decimal = Decimal("0")
    periodo: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


EVENT_CATALOG = {
    "nif_emitido": NifEmitido,
    "declaracao_submetida": DeclaracaoSubmetida,
    "pagamento_tributario_recebido": PagamentoTributarioRecebido,
}
