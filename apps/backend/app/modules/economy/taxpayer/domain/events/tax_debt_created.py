"""Domain Event: Dívida Fiscal Criada."""
from dataclasses import dataclass, field
from datetime import datetime, date
from uuid import UUID
from typing import Optional, Dict, Any
from decimal import Decimal

@dataclass
class TaxDebtCreated:
    """
    Evento de Domínio: Dívida fiscal criada.
    
    Este evento é disparado quando uma nova dívida fiscal é registrada
    para um contribuinte (ex: falta de pagamento, multa, juros).
    """
    debt_id: UUID
    taxpayer_id: UUID
    debt_number: str
    tax_type: str
    original_amount: Decimal
    current_amount: Decimal
    currency: str = 'AOA'
    interest: Optional[Decimal] = None
    fines: Optional[Decimal] = None
    created_date: date = field(default_factory=date.today)
    due_date: Optional[date] = None
    reason: Optional[str] = None
    related_declaration_id: Optional[UUID] = None
    created_by: Optional[UUID] = None
    occurred_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
    event_version: int = field(default=1)

    @property
    def event_type(self) -> str:
        """Tipo do evento."""
        return 'tax_debt.created'

    @property
    def aggregate_id(self) -> UUID:
        """ID do agregado associado."""
        return self.debt_id

    @property
    def total_amount(self) -> Decimal:
        """Total incluindo juros e multas."""
        total = self.current_amount
        if self.interest:
            total += self.interest
        if self.fines:
            total += self.fines
        return total

    def to_dict(self) -> Dict[str, Any]:
        """Converte o evento para dicionário."""
        return {'event_version': self.event_version, 'event_type': self.event_type, 'debt_id': str(self.debt_id), 'taxpayer_id': str(self.taxpayer_id), 'debt_number': self.debt_number, 'tax_type': self.tax_type, 'original_amount': str(self.original_amount), 'current_amount': str(self.current_amount), 'currency': self.currency, 'interest': str(self.interest) if self.interest else None, 'fines': str(self.fines) if self.fines else None, 'created_date': self.created_date.isoformat(), 'due_date': self.due_date.isoformat() if self.due_date else None, 'reason': self.reason, 'related_declaration_id': str(self.related_declaration_id) if self.related_declaration_id else None, 'created_by': str(self.created_by) if self.created_by else None, 'occurred_at': self.occurred_at.isoformat(), 'metadata': self.metadata}

    def __str__(self) -> str:
        """Representação em string."""
        return f'TaxDebtCreated(debt_number={self.debt_number}, tax_type={self.tax_type}, amount={self.current_amount} {self.currency}, at={self.occurred_at.isoformat()})'