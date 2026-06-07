from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


@dataclass
class LicencaEmitida:
    event_type: str = "licenca_emitida"
    version: int = 1
    licenca_id: UUID | None = None
    requerente_id: UUID | None = None
    tipo_licenca: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class ResidenciaConfirmada:
    event_type: str = "residencia_confirmada"
    version: int = 1
    cidadao_id: UUID | None = None
    municipio: str = ""
    provincia: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


@dataclass
class CertificadoMunicipalEmitido:
    event_type: str = "certificado_municipal_emitido"
    version: int = 1
    certificado_id: UUID | None = None
    requerente_id: UUID | None = None
    tipo_certificado: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: UUID = field(default_factory=uuid4)
    metadata: dict[str, Any] = field(default_factory=dict)
    correlation_id: UUID | None = None


EVENT_CATALOG = {
    "licenca_emitida": LicencaEmitida,
    "residencia_confirmada": ResidenciaConfirmada,
    "certificado_municipal_emitido": CertificadoMunicipalEmitido,
}
