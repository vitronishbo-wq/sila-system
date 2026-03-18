"""
Modelos de Domínio para Pagamentos.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any

from .enums import PaymentStatus, PaymentMethod, InvoiceStatus
from .exceptions import DomainValidationError


@dataclass
class Payment:
    """
    Entidade de Domínio representando um Pagamento.
    LIVRE DE DEPENDÊNCIAS DE ORM.
    
    REGRAS DE DOMÍNIO:
    - amount deve ser > 0
    - gateway_reference é obrigatória (idempotência)
    - status segue máquina de estados específica
    """
    id: str
    invoice_id: str
    citizen_id: str
    amount: float
    gateway_reference: str
    payment_method: str
    currency: str = "AOA"
    status: PaymentStatus = PaymentStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    confirmed_at: Optional[datetime] = None

    def __post_init__(self):
        self.validate()

    def validate(self):
        """Valida invariantes do domínio."""
        if self.amount <= 0:
            raise DomainValidationError(
                f"O valor do pagamento ({self.amount}) deve ser superior a zero."
            )
        if not self.gateway_reference or not self.gateway_reference.strip():
            raise DomainValidationError(
                "A referência do gateway é obrigatória."
            )

    def complete(self) -> Dict[str, Any]:
        """Finaliza o pagamento com sucesso."""
        if self.status != PaymentStatus.PENDING:
            raise DomainValidationError(
                f"Apenas pagamentos PENDENTES podem ser completados. "
                f"Status atual: {self.status.value}"
            )
        old_status = self.status
        self.status = PaymentStatus.COMPLETED
        self.confirmed_at = datetime.utcnow()
        return {
            "entity_type": "PAYMENT",
            "entity_id": self.id,
            "action": "PAYMENT_COMPLETED",
            "previous_state": {"status": old_status.value},
            "new_state": {"status": self.status.value},
            "timestamp": self.confirmed_at,
        }

    def fail(self, reason: str) -> Dict[str, Any]:
        """Marca o pagamento como falhado."""
        old_status = self.status
        self.status = PaymentStatus.FAILED
        return {
            "entity_type": "PAYMENT",
            "entity_id": self.id,
            "action": "PAYMENT_FAILED",
            "previous_state": {"status": old_status.value},
            "new_state": {"status": self.status.value, "reason": reason},
            "timestamp": datetime.utcnow(),
        }


@dataclass
class Invoice:
    """
    Entidade de Domínio representando uma Fatura.
    LIVRE DE DEPENDÊNCIAS DE ORM.
    
    REGRAS DE DOMÍNIO:
    - amount must be > 0
    - status segue máquina de estados específica
    - só pode ser paga se estiver PENDING ou OVERDUE
    """
    id: str
    reference: str
    citizen_id: str
    amount: float
    service_code: Optional[str] = None
    request_id: Optional[str] = None
    status: InvoiceStatus = InvoiceStatus.DRAFT
    currency: str = "AOA"
    created_at: datetime = field(default_factory=datetime.utcnow)
    issued_at: Optional[datetime] = None
    due_at: Optional[datetime] = None

    def __post_init__(self):
        self.validate()

    def validate(self):
        """Valida invariantes do domínio."""
        if self.amount <= 0:
            raise DomainValidationError(
                f"O valor da fatura ({self.amount}) deve ser superior a zero."
            )
        if not self.reference or not self.reference.strip():
            raise DomainValidationError("A referência da fatura é obrigatória.")

    def change_status(
        self, new_status: InvoiceStatus, reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """Muda o status da fatura com auditoria."""
        old_status = self.status
        self.status = new_status
        return {
            "entity_type": "INVOICE",
            "entity_id": self.id,
            "action": f"INVOICE_FLAGGED_{new_status.value.upper()}",
            "previous_state": {"status": old_status.value},
            "new_state": {"status": new_status.value},
            "reason": reason,
            "timestamp": datetime.utcnow(),
        }

    def is_payable(self) -> bool:
        """Verifica se a fatura pode ser paga."""
        return self.status in (
            InvoiceStatus.PENDING,
            InvoiceStatus.OVERDUE,
        )
