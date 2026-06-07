from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


@dataclass
class EmpresaRegistada:
    event_type: str = "empresa_registada"
    version: int = 1
    empresa_id: UUID | None = None
    nif: str = ""
    nome_empresa: str = ""
    tipo_sociedade: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class LicencaComercialEmitida:
    event_type: str = "licenca_comercial_emitida"
    version: int = 1
    licenca_id: UUID | None = None
    empresa_id: UUID | None = None
    tipo_licenca: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class ApoioConcedido:
    event_type: str = "apoio_concedido"
    version: int = 1
    apoio_id: UUID | None = None
    empresa_id: UUID | None = None
    tipo_apoio: str = ""
    valor: float = 0.0
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


EVENT_CATALOG = {
    "empresa_registada": EmpresaRegistada,
    "licenca_comercial_emitida": LicencaComercialEmitida,
    "apoio_concedido": ApoioConcedido,
}
