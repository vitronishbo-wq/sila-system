"""Domain Event: Declaração Fiscal Apresentada."""
from dataclasses import dataclass, field
from datetime import datetime, date
from uuid import UUID
from typing import Optional, Dict, Any
from decimal import Decimal

@dataclass
class TaxDeclarationFiled:
    """
    Evento de Domínio: Declaração fiscal apresentada.
    
    Este evento é disparado quando uma declaração fiscal é submetida
    com sucesso �\xa0 AGT.
    """
    declaration_id: UUID
    taxpayer_id: UUID
    declaration_number: str
    tax_type: str
    tax_period: str
    gross_amount: Decimal
    net_amount: Decimal
    deductions: Optional[Decimal] = None
    submission_date: date = field(default_factory=date.today)
    submitted_by: Optional[UUID] = None
    protocol_number: Optional[str] = None
    occurred_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
    event_version: int = field(default=1)

    @property
    def event_type(self) -> str:
        """Tipo do evento."""
        return 'tax_declaration.filed'

    @property
    def aggregate_id(self) -> UUID:
        """ID do agregado associado."""
        return self.declaration_id

    def to_dict(self) -> Dict[str, Any]:
        """Converte o evento para dicionário."""
        return {'event_version': self.event_version, 'event_type': self.event_type, 'declaration_id': str(self.declaration_id), 'taxpayer_id': str(self.taxpayer_id), 'declaration_number': self.declaration_number, 'tax_type': self.tax_type, 'tax_period': self.tax_period, 'gross_amount': str(self.gross_amount), 'net_amount': str(self.net_amount), 'deductions': str(self.deductions) if self.deductions else None, 'submission_date': self.submission_date.isoformat(), 'submitted_by': str(self.submitted_by) if self.submitted_by else None, 'protocol_number': self.protocol_number, 'occurred_at': self.occurred_at.isoformat(), 'metadata': self.metadata}

    def __str__(self) -> str:
        """Representação em string."""
        return f'TaxDeclarationFiled(declaration_number={self.declaration_number}, tax_type={self.tax_type}, period={self.tax_period}, at={self.occurred_at.isoformat()})'