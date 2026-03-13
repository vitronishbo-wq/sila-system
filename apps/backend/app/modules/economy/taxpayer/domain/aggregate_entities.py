"""Base Classes para o Aggregate Taxpayer"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any
from uuid import UUID, uuid4

@dataclass
class AggregateEntity(ABC):
    """
    Base class para entidades dentro do Aggregate Root (Taxpayer).
    
    Uma entidade agregada tem:
    - ID único dentro do contexto do Taxpayer
    - Não tem repositório próprio
    - Sempre acessada via Taxpayer
    - Ciclo de vida gerenciado pelo Taxpayer
    """
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None
    version: int = 1

    @abstractmethod
    def validate(self) -> None:
        """
        Valida as invariantes da entidade.
        Deve ser chamado pelo Taxpayer antes de aplicar mudanças.
        
        Raises:
            ValueError: Se alguma invariante é violada
        """
        pass

    def mark_updated(self, by: Optional[UUID]=None) -> None:
        """Marca a entidade como atualizada."""
        self.updated_at = datetime.utcnow()
        self.updated_by = by
        self.version += 1

    def to_dict(self) -> dict[str, Any]:
        """Serializa a entidade (para persistência)."""
        return {'id': str(self.id), 'created_at': self.created_at.isoformat(), 'updated_at': self.updated_at.isoformat() if self.updated_at else None, 'created_by': str(self.created_by) if self.created_by else None, 'updated_by': str(self.updated_by) if self.updated_by else None, 'version': self.version}

@dataclass
class TaxDeclaration(AggregateEntity):
    """
    Declaração fiscal de um contribuinte.
    
    NÃO é um agregado separado, é entidade dentro de Taxpayer.
    """
    declaration_number: str = ''
    tax_type: str = ''
    tax_period: str = ''
    declaration_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    gross_amount: float = 0.0
    deductions: Optional[float] = None
    net_amount: float = 0.0
    status: str = 'DRAFT'
    submitted_by: Optional[UUID] = None
    submitted_at: Optional[datetime] = None
    metadata: dict = field(default_factory=dict)

    def validate(self) -> None:
        """Valida a declaração."""
        if not self.declaration_number:
            raise ValueError('Número de declaração é obrigatório')
        if not self.tax_type:
            raise ValueError('Tipo de imposto é obrigatório')
        if not self.tax_period:
            raise ValueError('Período fiscal é obrigatório')
        if self.gross_amount < 0:
            raise ValueError('Valor bruto não pode ser negativo')
        if self.net_amount < 0:
            raise ValueError('Valor líquido não pode ser negativo')

    def to_dict(self) -> dict[str, Any]:
        """Serializa declaração."""
        base = super().to_dict()
        base.update({'declaration_number': self.declaration_number, 'tax_type': self.tax_type, 'tax_period': self.tax_period, 'declaration_date': self.declaration_date.isoformat() if self.declaration_date else None, 'due_date': self.due_date.isoformat() if self.due_date else None, 'gross_amount': self.gross_amount, 'deductions': self.deductions, 'net_amount': self.net_amount, 'status': self.status, 'submitted_by': str(self.submitted_by) if self.submitted_by else None, 'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None, 'metadata': self.metadata})
        return base

@dataclass
class TaxDebt(AggregateEntity):
    """
    Débito fiscal de um contribuinte.
    
    NÃO é um agregado separado, é entidade dentro de Taxpayer.
    """
    debt_number: str = ''
    tax_type: str = ''
    original_amount: float = 0.0
    current_amount: float = 0.0
    interest: Optional[float] = None
    fines: Optional[float] = None
    created_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    status: str = 'OPEN'
    related_declaration_id: Optional[UUID] = None
    metadata: dict = field(default_factory=dict)

    def validate(self) -> None:
        """Valida o débito."""
        if not self.debt_number:
            raise ValueError('Número de débito é obrigatório')
        if not self.tax_type:
            raise ValueError('Tipo de imposto é obrigatório')
        if self.original_amount < 0:
            raise ValueError('Valor original não pode ser negativo')
        if self.current_amount < 0:
            raise ValueError('Valor atual não pode ser negativo')
        if self.current_amount > self.original_amount * 2:
            raise ValueError('Valor atual muito alto em relação ao original')

    @property
    def total_amount(self) -> float:
        """Retorna o valor total incluindo juros e multas."""
        total = self.current_amount
        if self.interest:
            total += self.interest
        if self.fines:
            total += self.fines
        return total

    def to_dict(self) -> dict[str, Any]:
        """Serializa débito."""
        base = super().to_dict()
        base.update({'debt_number': self.debt_number, 'tax_type': self.tax_type, 'original_amount': self.original_amount, 'current_amount': self.current_amount, 'interest': self.interest, 'fines': self.fines, 'created_date': self.created_date.isoformat() if self.created_date else None, 'due_date': self.due_date.isoformat() if self.due_date else None, 'status': self.status, 'related_declaration_id': str(self.related_declaration_id) if self.related_declaration_id else None, 'metadata': self.metadata})
        return base

@dataclass
class TaxPayment(AggregateEntity):
    """
    Pagamento fiscal de um contribuinte.
    
    NÃO é um agregado separado, é entidade dentro de Taxpayer.
    """
    payment_number: str = ''
    payment_method: str = ''
    amount: float = 0.0
    payment_date: Optional[datetime] = None
    status: str = 'PENDING'
    reference: Optional[str] = None
    related_declaration_id: Optional[UUID] = None
    related_debt_id: Optional[UUID] = None
    paid_by: Optional[UUID] = None
    metadata: dict = field(default_factory=dict)

    def validate(self) -> None:
        """Valida o pagamento."""
        if not self.payment_number:
            raise ValueError('Número de pagamento é obrigatório')
        if not self.payment_method:
            raise ValueError('Método de pagamento é obrigatório')
        if self.amount <= 0:
            raise ValueError('Valor de pagamento deve ser positivo')

    def to_dict(self) -> dict[str, Any]:
        """Serializa pagamento."""
        base = super().to_dict()
        base.update({'payment_number': self.payment_number, 'payment_method': self.payment_method, 'amount': self.amount, 'payment_date': self.payment_date.isoformat() if self.payment_date else None, 'status': self.status, 'reference': self.reference, 'related_declaration_id': str(self.related_declaration_id) if self.related_declaration_id else None, 'related_debt_id': str(self.related_debt_id) if self.related_debt_id else None, 'paid_by': str(self.paid_by) if self.paid_by else None, 'metadata': self.metadata})
        return base

@dataclass
class TaxCertificate(AggregateEntity):
    """
    Certidão fiscal de um contribuinte.
    
    NÃO é um agregado separado, é entidade dentro de Taxpayer.
    """
    certificate_number: str = ''
    certificate_type: str = ''
    issued_at: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    status: str = 'VALID'
    protocol_number: Optional[str] = None
    issued_by: Optional[UUID] = None
    metadata: dict = field(default_factory=dict)

    def validate(self) -> None:
        """Valida a certidão."""
        if not self.certificate_number:
            raise ValueError('Número de certidão é obrigatório')
        if not self.certificate_type:
            raise ValueError('Tipo de certidão é obrigatório')

    def is_valid_at(self, check_date: datetime) -> bool:
        """Verifica se a certidão é válida em uma data específica."""
        if self.status != 'VALID':
            return False
        if not self.valid_until:
            return True
        return check_date <= self.valid_until

    def to_dict(self) -> dict[str, Any]:
        """Serializa certidão."""
        base = super().to_dict()
        base.update({'certificate_number': self.certificate_number, 'certificate_type': self.certificate_type, 'issued_at': self.issued_at.isoformat() if self.issued_at else None, 'valid_until': self.valid_until.isoformat() if self.valid_until else None, 'status': self.status, 'protocol_number': self.protocol_number, 'issued_by': str(self.issued_by) if self.issued_by else None, 'metadata': self.metadata})
        return base