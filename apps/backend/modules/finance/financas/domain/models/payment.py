from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from app.modules.financas.domain.models.enums import PaymentStatus
from app.modules.financas.exceptions import DomainValidationError

@dataclass
class Payment:
    """
    Entidade de Domínio representando um Pagamento no Sistema SILA.
    LIVRE DE DEPENDÊNCIAS DE ORM.
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
        if self.amount <= 0:
            raise DomainValidationError(f"O valor do pagamento ({self.amount}) deve ser superior a zero.")
        
        if not self.gateway_reference or not self.gateway_reference.strip():
            raise DomainValidationError("A referência do gateway é obrigatória.")

    def complete(self) -> Dict[str, Any]:
        """
        Finaliza o pagamento com sucesso.
        """
        if self.status != PaymentStatus.PENDING:
            raise DomainValidationError(f"Apenas pagamentos PENDENTES podem ser completados. Status atual: {self.status.value}")
        
        old_status = self.status
        self.status = PaymentStatus.COMPLETED
        self.confirmed_at = datetime.utcnow()

        return {
            "entity_type": "PAYMENT",
            "entity_id": self.id,
            "action": "PAYMENT_COMPLETED",
            "previous_state": {"status": old_status.value},
            "new_state": {"status": self.status.value},
            "timestamp": self.confirmed_at
        }

    def fail(self, reason: str) -> Dict[str, Any]:
        """
        Marca o pagamento como falhado.
        """
        old_status = self.status
        self.status = PaymentStatus.FAILED
        
        return {
            "entity_type": "PAYMENT",
            "entity_id": self.id,
            "action": "PAYMENT_FAILED",
            "previous_state": {"status": old_status.value},
            "new_state": {"status": self.status.value, "reason": reason},
            "timestamp": datetime.utcnow()
        }