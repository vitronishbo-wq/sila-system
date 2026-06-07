"""Domain Event: Contribuinte Registrado."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID


@dataclass
class TaxpayerRegistered:
    """
    Evento de Domínio: Contribuinte registrado no sistema.

    Este evento é disparado quando um novo contribuinte é registrado
    com sucesso no SILA.
    """

    taxpayer_id: UUID
    nif: str
    name: str
    registered_by: UUID | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    tax_regime: str | None = None
    occurred_at: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)
    event_version: int = field(default=1)

    @property
    def event_type(self) -> str:
        """Tipo do evento."""
        return "taxpayer.registered"

    @property
    def aggregate_id(self) -> UUID:
        """ID do agregado associado."""
        return self.taxpayer_id

    def to_dict(self) -> dict[str, Any]:
        """Converte o evento para dicionário."""
        return {
            "event_version": self.event_version,
            "event_type": self.event_type,
            "taxpayer_id": str(self.taxpayer_id),
            "nif": self.nif,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "tax_regime": self.tax_regime,
            "registered_by": str(self.registered_by) if self.registered_by else None,
            "occurred_at": self.occurred_at.isoformat(),
            "metadata": self.metadata,
        }

    def __str__(self) -> str:
        """Representação em string."""
        return f"TaxpayerRegistered(nif={self.nif}, name={self.name}, at={self.occurred_at.isoformat()})"
