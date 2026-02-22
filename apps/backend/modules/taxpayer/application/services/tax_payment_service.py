from typing import Optional, List
from uuid import UUID
from datetime import datetime
import logging

from ..ports.taxpayer_repository_port import TaxpayerRepositoryPort
from ..ports.agt_integration_port import AGTIntegrationPort
from ..ports.notification_port import NotificationPort
from ..ports.audit_port import AuditPort


class TaxPaymentService:
    """Serviço de pagamentos fiscais"""
    
    def __init__(
        self,
        repo: TaxpayerRepositoryPort,
        agt: AGTIntegrationPort,
        notification: NotificationPort,
        audit: AuditPort
    ):
        self.repo = repo
        self.agt = agt
        self.notification = notification
        self.audit = audit
        self.logger = logging.getLogger(__name__)
    
    async def process_payment(
        self,
        taxpayer_id: UUID,
        amount: float,
        payment_method: str,
        paid_by: UUID,
        debt_ids: Optional[List[UUID]] = None,
        reference: Optional[str] = None,
        metadata: Optional[dict] = None,
        ip_address: Optional[str] = None
    ) -> List[object]:
        """Processa um pagamento (pode ser para múltiplas dívidas)"""
        self.logger.info(f"Processando pagamento de {amount} para taxpayer {taxpayer_id}")
        
        taxpayer = await self.repo.find_by_id(taxpayer_id)
        if not taxpayer:
            raise ValueError("Contribuinte não encontrado")
        
        if not debt_ids:
            debts, _ = await self.repo.find_debts_by_taxpayer(taxpayer_id, include_paid=False)
            debt_ids = [d for d in (debts or [])]
        
        remaining_amount = amount
        payments = []
        
        for debt_id in debt_ids:
            if remaining_amount <= 0:
                break
            
            debt = await self.repo.find_debt_by_id(debt_id)
            if not debt:
                continue
            
            payment_amount = min(remaining_amount, debt.get('current_amount', 0))
            
            if payment_amount > 0:
                payments.append({
                    "taxpayer_id": str(taxpayer_id),
                    "debt_id": str(debt_id),
                    "amount": payment_amount
                })
                remaining_amount -= payment_amount
        
        if not payments:
            raise ValueError("Nenhum pagamento foi processado")
        
        await self.notification.notify_payment_received(
            taxpayer_id,
            sum(p["amount"] for p in payments),
            reference or "PAY-AUTO"
        )
        
        await self.audit.log(
            action="PAYMENT_PROCESSED",
            user_id=paid_by,
            entity_id=taxpayer_id,
            entity_type="taxpayer",
            details={"total_amount": amount, "payments": len(payments), "method": payment_method},
            ip_address=ip_address
        )
        
        return payments
    
    async def get_payment(self, payment_id: UUID) -> Optional[object]:
        """Busca pagamento por ID"""
        return await self.repo.find_payment_by_id(payment_id)
    
    async def get_taxpayer_payments(
        self,
        taxpayer_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[object]:
        """Lista pagamentos de um contribuinte"""
        payments, _ = await self.repo.find_payments_by_taxpayer(taxpayer_id, skip, limit)
        return payments
    
    async def reverse_payment(
        self,
        payment_id: UUID,
        reason: str,
        reversed_by: UUID,
        ip_address: Optional[str] = None
    ) -> object:
        """Estorna um pagamento"""
        payment = await self.repo.find_payment_by_id(payment_id)
        if not payment:
            raise ValueError("Pagamento não encontrado")
        
        await self.notification.notify_taxpayer(
            payment.get('taxpayer_id'),
            "Pagamento Estornado",
            f"O pagamento foi estornado: {reason}"
        )
        
        await self.audit.log(
            action="PAYMENT_REVERSED",
            user_id=reversed_by,
            entity_id=payment_id,
            entity_type="tax_payment",
            details={"reason": reason},
            ip_address=ip_address
        )
        
        return {"status": "reversed", "payment_id": str(payment_id)}
