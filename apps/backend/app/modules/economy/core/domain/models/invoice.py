from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from app.modules.economy.domain.models.enums import InvoiceStatus
from app.modules.economy.domain.exceptions import DomainValidationError

@dataclass
class Invoice:
    """
    Entidade de Domínio representando uma Fatura Oficial no Sistema SILA.
    Contém campos obrigatórios para classificação orçamental e integração com o Tesouro Nacional.
    LIVRE DE DEPENDÊNCIAS DE ORM (SQLAlchemy).
    """
    id: str
    citizen_id: str
    reference: str
    revenue_code: str
    cost_center: str
    service_code: str
    service_name: str
    amount: float
    due_date: datetime
    request_id: Optional[str] = None
    currency: str = 'AOA'
    status: InvoiceStatus = InvoiceStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    paid_at: Optional[datetime] = None

    def __post_init__(self):
        self.validate()

    def validate(self):
        if self.amount <= 0:
            raise DomainValidationError(f'O montante da fatura ({self.amount}) deve ser superior a zero.')
        if not self.currency or len(self.currency) != 3:
            raise DomainValidationError(f'Código de moeda ISO 4217 inválido: {self.currency}')
        if not self.revenue_code or not self.revenue_code.strip():
            raise DomainValidationError('O código de receita (revenue_code) é obrigatório.')
        if not self.cost_center or not self.cost_center.strip():
            raise DomainValidationError('O centro de custo (cost_center) é obrigatório.')

    def change_status(self, new_status: InvoiceStatus, reason: str='') -> Dict[str, Any]:
        """
        Executa a transição de estado da fatura e retorna os dados para auditoria.
        Regra: PAID e CANCELLED são estados finais.
        """
        valid_transitions = {InvoiceStatus.PENDING: [InvoiceStatus.PAID, InvoiceStatus.CANCELLED, InvoiceStatus.OVERDUE], InvoiceStatus.OVERDUE: [InvoiceStatus.PAID, InvoiceStatus.CANCELLED], InvoiceStatus.PAID: [], InvoiceStatus.CANCELLED: []}
        if new_status not in valid_transitions.get(self.status, []):
            from app.modules.economy.domain.exceptions import InvalidInvoiceStateError
            raise InvalidInvoiceStateError(current_status=self.status.value, action=f'mudar para {new_status.value}')
        old_status = self.status
        self.status = new_status
        self.updated_at = datetime.utcnow()
        if new_status == InvoiceStatus.PAID:
            self.paid_at = datetime.utcnow()
        return {'entity_type': 'INVOICE', 'entity_id': self.id, 'action': 'STATUS_CHANGE', 'previous_state': {'status': old_status.value}, 'new_state': {'status': new_status.value, 'reason': reason}, 'timestamp': self.updated_at}

    def is_overdue(self) -> bool:
        return self.status == InvoiceStatus.PENDING and datetime.utcnow() > self.due_date
