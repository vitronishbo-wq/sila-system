"""Domain Event: Contribuinte Registrado."""
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from typing import Optional, Dict, Any


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
    registered_by: Optional[UUID] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    tax_regime: Optional[str] = None
    occurred_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
    event_version: int = field(default=1)  # Versionamento para evolução futura

    @property
    def event_type(self) -> str:
        """Tipo do evento."""
        return "taxpayer.registered"

    @property
    def aggregate_id(self) -> UUID:
        """ID do agregado associado."""
        return self.taxpayer_id

    def to_dict(self) -> Dict[str, Any]:
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
        return (
            f"TaxpayerRegistered(nif={self.nif}, name={self.name}, "
            f"at={self.occurred_at.isoformat()})"
        )
