from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


@dataclass
class NascimentoRegistado:
    event_type: str = "nascimento_registado"
    version: int = 1
    registo_id: UUID | None = None
    cidadao_nome: str = ""
    data_nascimento: str = ""
    local_nascimento: str = ""
    nome_pai: str = ""
    nome_mae: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class CasamentoRegistado:
    event_type: str = "casamento_registado"
    version: int = 1
    registo_id: UUID | None = None
    conjuge1_nome: str = ""
    conjuge2_nome: str = ""
    data_casamento: str = ""
    regime_bens: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class ObitoRegistado:
    event_type: str = "obito_registado"
    version: int = 1
    registo_id: UUID | None = None
    cidadao_nome: str = ""
    data_obito: str = ""
    causa: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


EVENT_CATALOG = {
    "nascimento_registado": NascimentoRegistado,
    "casamento_registado": CasamentoRegistado,
    "obito_registado": ObitoRegistado,
}
