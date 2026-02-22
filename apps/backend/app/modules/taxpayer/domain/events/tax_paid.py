"""Domain Event: Imposto Pago."""
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from typing import Optional, Dict, Any
from decimal import Decimal


@dataclass
class TaxPaid:
    """
    Evento de Domínio: Imposto pago com sucesso.
    
    Este evento é disparado quando um pagamento de imposto é
    confirmado.
    """
    payment_id: UUID
    taxpayer_id: UUID
    tax_type: str
    amount: Decimal
    currency: str = "AOA"
    payment_method: Optional[str] = None
    payment_reference: Optional[str] = None
    tax_period: Optional[str] = None
    declaration_id: Optional[UUID] = None
    debt_id: Optional[UUID] = None
    paid_by: Optional[UUID] = None
    payment_date: datetime = field(default_factory=datetime.utcnow)
    occurred_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
    event_version: int = field(default=1)  # Versionamento para evolução futura

    @property
    def event_type(self) -> str:
        """Tipo do evento."""
        return "tax.paid"

    @property
    def aggregate_id(self) -> UUID:
        """ID do agregado associado."""
        return self.payment_id

    def to_dict(self) -> Dict[str, Any]:
        """Converte o evento para dicionário."""
        return {
            "event_version": self.event_version,
            "event_type": self.event_type,
            "payment_id": str(self.payment_id),
            "taxpayer_id": str(self.taxpayer_id),
            "tax_type": self.tax_type,
            "amount": str(self.amount),
            "currency": self.currency,
            "payment_method": self.payment_method,
            "payment_reference": self.payment_reference,
            "tax_period": self.tax_period,
            "declaration_id": str(self.declaration_id) if self.declaration_id else None,
            "debt_id": str(self.debt_id) if self.debt_id else None,
            "paid_by": str(self.paid_by) if self.paid_by else None,
            "payment_date": self.payment_date.isoformat(),
            "occurred_at": self.occurred_at.isoformat(),
            "metadata": self.metadata,
        }

    def __str__(self) -> str:
        """Representação em string."""
        return (
            f"TaxPaid(tax_type={self.tax_type}, amount={self.amount} {self.currency}, "
            f"at={self.occurred_at.isoformat()})"
        )
