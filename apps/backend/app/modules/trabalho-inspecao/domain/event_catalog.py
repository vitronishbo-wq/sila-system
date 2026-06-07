from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


@dataclass
class InspecaoAgendada:
    event_type: str = "inspecao_agendada"
    version: int = 1
    inspecao_id: UUID | None = None
    empregador_id: UUID | None = None
    tipo_inspecao: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class InspecaoRealizada:
    event_type: str = "inspecao_realizada"
    version: int = 1
    inspecao_id: UUID | None = None
    empregador_id: UUID | None = None
    resultado: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class AutoInfracaoEmitido:
    event_type: str = "auto_infracao_emitido"
    version: int = 1
    auto_id: UUID | None = None
    empregador_id: UUID | None = None
    valor_multa: float = 0.0
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


EVENT_CATALOG = {"inspecao_agendada": InspecaoAgendada,
                 "inspecao_realizada": InspecaoRealizada,
                 "auto_infracao_emitido": AutoInfracaoEmitido}
