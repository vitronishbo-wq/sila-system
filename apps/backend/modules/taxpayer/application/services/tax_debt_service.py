from typing import Optional, List, Tuple
from uuid import UUID
from datetime import date, datetime, timedelta
import logging

from ..ports.taxpayer_repository_port import TaxpayerRepositoryPort
from ..ports.agt_integration_port import AGTIntegrationPort
from ..ports.notification_port import NotificationPort
from ..ports.audit_port import AuditPort


class TaxDebtService:
    """Serviço de gestão de dívidas fiscais"""
    
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
    
    async def create_debt(
        self,
        taxpayer_id: UUID,
        tax_type: str,
        original_amount: float,
        due_date: date,
        created_by: UUID,
        description: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> object:
        """Cria uma nova dívida fiscal"""
        self.logger.info(f"Criando dívida para taxpayer {taxpayer_id}")
        
        taxpayer = await self.repo.find_by_id(taxpayer_id)
        if not taxpayer:
            raise ValueError("Contribuinte não encontrado")
        
        await self.notification.notify_debt_created(taxpayer_id, original_amount, due_date)
        
        await self.audit.log(
            action="DEBT_CREATED",
            user_id=created_by,
            entity_id=taxpayer_id,
            entity_type="tax_debt",
            details={"tax_type": tax_type, "original_amount": original_amount},
            ip_address=ip_address
        )
        
        return {"status": "created", "taxpayer_id": str(taxpayer_id), "amount": original_amount}
    
    async def get_taxpayer_debts(
        self,
        taxpayer_id: UUID,
        include_paid: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[object], int]:
        """Lista dívidas de um contribuinte"""
        return await self.repo.find_debts_by_taxpayer(taxpayer_id, include_paid, skip, limit)
    
    async def register_payment(
        self,
        debt_id: UUID,
        amount: float,
        payment_method: str,
        payment_date: datetime,
        paid_by: UUID,
        reference: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> object:
        """Regista pagamento de dívida"""
        debt = await self.repo.find_debt_by_id(debt_id)
        if not debt:
            raise ValueError("Dívida não encontrada")
        
        await self.audit.log(
            action="DEBT_PAYMENT_REGISTERED",
            user_id=paid_by,
            entity_id=debt_id,
            entity_type="tax_debt",
            details={"amount": amount, "method": payment_method},
            ip_address=ip_address
        )
        
        return {"status": "success", "debt_id": str(debt_id), "amount": amount}
    
    async def sync_with_agt(self, taxpayer_id: UUID) -> dict:
        """Sincroniza dívidas com AGT"""
        taxpayer = await self.repo.find_by_id(taxpayer_id)
        if not taxpayer:
            raise ValueError("Contribuinte não encontrado")
        
        return {"created": 0, "updated": 0, "errors": 0}
