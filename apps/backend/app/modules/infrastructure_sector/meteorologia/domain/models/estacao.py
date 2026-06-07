from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from apps.backend.app.modules.infrastructure_sector.meteorologia.domain.enums import StationStatus


def _utcnow() -> datetime:
    return datetime.now(UTC)


class EstacaoMeteorologica:
    """Entidade de dominio para estacao meteorologica."""

    def __init__(
        self,
        *,
        estacao_id: UUID | None = None,
        codigo: str | None = None,
        nome: str | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
        altitude: float | None = None,
        status: StationStatus = StationStatus.ACTIVE,
        municipio: str | None = None,
        provincia: str | None = None,
        metadata: dict[str, Any] | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        self.id = estacao_id or uuid4()
        self.codigo = codigo
        self.nome = nome
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.status = status
        self.municipio = municipio
        self.provincia = provincia
        self.metadata = metadata or {}
        self.created_at = created_at or _utcnow()
        self.updated_at = updated_at or self.created_at

    @property
    def is_active(self) -> bool:
        return self.status == StationStatus.ACTIVE

    def activate(self) -> None:
        self.status = StationStatus.ACTIVE
        self.updated_at = _utcnow()

    def deactivate(self, reason: str | None = None) -> None:
        self.status = StationStatus.INACTIVE
        if reason:
            self.metadata["deactivation_reason"] = reason
        self.updated_at = _utcnow()

    def set_maintenance(self) -> None:
        self.status = StationStatus.MAINTENANCE
        self.updated_at = _utcnow()

    def update_location(
        self, *, latitude: float, longitude: float, altitude: float | None = None
    ) -> None:
        if not -90 <= latitude <= 90:
            raise ValueError(f"Latitude invalida: {latitude}")
        if not -180 <= longitude <= 180:
            raise ValueError(f"Longitude invalida: {longitude}")
        self.latitude = latitude
        self.longitude = longitude
        if altitude is not None:
            self.altitude = altitude
        self.updated_at = _utcnow()

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": str(self.id),
            "codigo": self.codigo,
            "nome": self.nome,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "altitude": self.altitude,
            "status": self.status.value,
            "municipio": self.municipio,
            "provincia": self.provincia,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "metadata": self.metadata,
        }
