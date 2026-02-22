from typing import Optional, List, Tuple
from uuid import UUID
from datetime import datetime
import logging

from ..ports.taxpayer_repository_port import TaxpayerRepositoryPort
from ..ports.agt_integration_port import AGTIntegrationPort
from ..ports.notification_port import NotificationPort
from ..ports.audit_port import AuditPort


class TaxDeclarationService:
    """Serviço de declarações fiscais"""
    
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
    
    async def submit_declaration(
        self,
        taxpayer_id: UUID,
        tax_type: str,
        tax_period: str,
        gross_amount: float,
        deductions: Optional[float],
        submitted_by: UUID,
        ip_address: Optional[str] = None
    ) -> object:
        """Submete uma nova declaração fiscal"""
        self.logger.info(f"Submetendo declaração para taxpayer {taxpayer_id}")
        
        taxpayer = await self.repo.find_by_id(taxpayer_id)
        if not taxpayer:
            raise ValueError("Contribuinte não encontrado")
        
        net_amount = (gross_amount or 0) - (deductions or 0)
        
        await self.notification.notify_taxpayer(
            taxpayer_id,
            "Declaração Submetida",
            f"Sua declaração de {tax_type} para {tax_period} foi submetida com sucesso"
        )
        
        await self.audit.log(
            action="DECLARATION_SUBMITTED",
            user_id=submitted_by,
            entity_id=taxpayer_id,
            entity_type="tax_declaration",
            details={"tax_type": tax_type, "gross_amount": gross_amount, "net_amount": net_amount},
            ip_address=ip_address
        )
        
        return {"status": "submitted", "taxpayer_id": str(taxpayer_id), "tax_type": tax_type}
    
    async def process_declaration(
        self,
        declaration_id: UUID,
        status: str,
        processed_by: UUID,
        observations: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> object:
        """Processa uma declaração (aprova/rejeita)"""
        self.logger.info(f"Processando declaração {declaration_id}")
        
        await self.audit.log(
            action=f"DECLARATION_{status}",
            user_id=processed_by,
            entity_id=declaration_id,
            entity_type="tax_declaration",
            details={"new_status": status, "observations": observations},
            ip_address=ip_address
        )
        
        return {"status": status, "declaration_id": str(declaration_id)}
    
    async def get_taxpayer_declarations(
        self,
        taxpayer_id: UUID,
        year: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[object], int]:
        """Lista declarações de um contribuinte"""
        return await self.repo.find_declarations_by_taxpayer(taxpayer_id, year, skip, limit)
