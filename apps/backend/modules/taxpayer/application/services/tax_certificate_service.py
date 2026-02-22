from typing import Optional, List, Tuple
from uuid import UUID
from datetime import datetime, date, timedelta
import logging

from ..ports.taxpayer_repository_port import TaxpayerRepositoryPort
from ..ports.agt_integration_port import AGTIntegrationPort
from ..ports.notification_port import NotificationPort
from ..ports.audit_port import AuditPort


class TaxCertificateService:
    """Serviço de certidões fiscais"""
    
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
    
    async def request_certificate(
        self,
        taxpayer_id: UUID,
        certificate_type: str,
        year: Optional[int],
        requested_by: UUID,
        purpose: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> object:
        """Solicita uma certidão fiscal"""
        self.logger.info(f"Solicitando certidão para taxpayer {taxpayer_id}")
        
        taxpayer = await self.repo.find_by_id(taxpayer_id)
        if not taxpayer:
            raise ValueError("Contribuinte não encontrado")
        
        await self.notification.notify_taxpayer(
            taxpayer_id,
            "Certidão Solicitada",
            f"Sua certidão {certificate_type} foi solicitada com sucesso"
        )
        
        await self.audit.log(
            action="CERTIFICATE_REQUESTED",
            user_id=requested_by,
            entity_id=taxpayer_id,
            entity_type="tax_certificate",
            details={"certificate_type": certificate_type, "year": year, "purpose": purpose},
            ip_address=ip_address
        )
        
        return {"status": "requested", "taxpayer_id": str(taxpayer_id), "type": certificate_type}
    
    async def process_certificate(
        self,
        certificate_id: UUID,
        status: str,
        processed_by: UUID,
        file_url: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> object:
        """Processa uma certidão (emite/rejeita)"""
        await self.audit.log(
            action=f"CERTIFICATE_{status}",
            user_id=processed_by,
            entity_id=certificate_id,
            entity_type="tax_certificate",
            details={"new_status": status, "file_url": file_url},
            ip_address=ip_address
        )
        
        return {"status": status, "certificate_id": str(certificate_id)}
    
    async def get_taxpayer_certificates(
        self,
        taxpayer_id: UUID,
        certificate_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Tuple[List[object], int]:
        """Lista certidões de um contribuinte"""
        return await self.repo.find_certificates_by_taxpayer(
            taxpayer_id, certificate_type, skip, limit
        )
