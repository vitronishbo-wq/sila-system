from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


@dataclass
class ComercioRegistado:
    event_type: str = "comercio_registado"
    version: int = 1
    comercio_id: UUID | None = None
    nif: str = ""
    nome_comercial: str = ""
    ramo_actividade: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class AlvaraEmitido:
    event_type: str = "alvara_emitido"
    version: int = 1
    alvara_id: UUID | None = None
    comercio_id: UUID | None = None
    tipo_alvara: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class InspecaoComercialRealizada:
    event_type: str = "inspecao_comercial_realizada"
    version: int = 1
    inspecao_id: UUID | None = None
    comercio_id: UUID | None = None
    resultado: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


EVENT_CATALOG = {
    "comercio_registado": ComercioRegistado,
    "alvara_emitido": AlvaraEmitido,
    "inspecao_comercial_realizada": InspecaoComercialRealizada,
}
