from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


@dataclass
class ContratoTrabalhoRegistado:
    event_type: str = "contrato_trabalho_registado"
    version: int = 1
    contrato_id: UUID | None = None
    cidadao_id: UUID | None = None
    empregador_id: UUID | None = None
    tipo_contrato: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class VagaEmpregoCriada:
    event_type: str = "vaga_emprego_criada"
    version: int = 1
    vaga_id: UUID | None = None
    empregador_id: UUID | None = None
    cargo: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class ColocacaoRealizada:
    event_type: str = "colocacao_realizada"
    version: int = 1
    colocacao_id: UUID | None = None
    cidadao_id: UUID | None = None
    vaga_id: UUID | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


EVENT_CATALOG = {"contrato_trabalho_registado": ContratoTrabalhoRegistado,
                 "vaga_emprego_criada": VagaEmpregoCriada,
                 "colocacao_realizada": ColocacaoRealizada}
