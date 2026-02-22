from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime, timedelta
import asyncio
import logging

from ...domain.entities.taxpayer import Taxpayer
from ..ports.taxpayer_repository_port import TaxpayerRepositoryPort
from ..ports.agt_integration_port import AGTIntegrationPort
from ..ports.audit_port import AuditPort


class AGTSyncService:
    """Serviço de sincronização com AGT"""
    
    def __init__(
        self,
        repo: TaxpayerRepositoryPort,
        agt: AGTIntegrationPort,
        audit: AuditPort
    ):
        self.repo = repo
        self.agt = agt
        self.audit = audit
        self.logger = logging.getLogger(__name__)
    
    async def sync_all_taxpayers(self, batch_size: int = 100) -> Dict[str, Any]:
        """Sincroniza todos os contribuintes com a AGT"""
        self.logger.info("Iniciando sincronização em massa com AGT")
        
        results = {
            "total_processed": 0,
            "success": 0,
            "errors": 0,
            "details": []
        }
        
        page = 0
        while True:
            taxpayers, total = await self.repo.list_all(
                skip=page * batch_size,
                limit=batch_size
            )
            
            if not taxpayers:
                break
            
            for taxpayer in taxpayers:
                try:
                    result = await self.sync_taxpayer(taxpayer.id)
                    results["success"] += 1
                except Exception as e:
                    self.logger.error(f"Erro ao sincronizar: {str(e)}")
                    results["errors"] += 1
                
                results["total_processed"] += 1
            
            page += 1
            await asyncio.sleep(0.1)
        
        self.logger.info(f"Sincronização concluída: {results}")
        
        await self.audit.log(
            action="AGT_BULK_SYNC",
            user_id=None,
            entity_id=None,
            entity_type="system",
            details=results
        )
        
        return results
    
    async def sync_taxpayer(self, taxpayer_id: UUID) -> Dict[str, Any]:
        """Sincroniza um contribuinte específico com a AGT"""
        self.logger.info(f"Sincronizando taxpayer {taxpayer_id}")
        
        taxpayer = await self.repo.find_by_id(taxpayer_id)
        if not taxpayer:
            raise ValueError("Contribuinte não encontrado")
        
        updates = {}
        
        agt_data = await self.agt.get_taxpayer_data(taxpayer.nif)
        if agt_data:
            if agt_data.get('name') and agt_data['name'] != taxpayer.name:
                updates['name'] = agt_data['name']
            if agt_data.get('status') and agt_data['status'] != taxpayer.status:
                updates['status'] = agt_data['status']
        
        if updates:
            for key, value in updates.items():
                setattr(taxpayer, key, value)
            taxpayer.updated_at = datetime.now()
            await self.repo.save(taxpayer)
        
        self.logger.info(f"Taxpayer {taxpayer.nif} sincronizado")
        
        await self.audit.log(
            action="AGT_SYNC",
            user_id=None,
            entity_id=taxpayer_id,
            entity_type="taxpayer",
            details={"updates": updates}
        )
        
        return updates
    
    async def check_agt_health(self) -> Dict[str, Any]:
        """Verifica saúde da integração com AGT"""
        is_healthy = await self.agt.health_check()
        
        return {
            "service": "AGT",
            "status": "healthy" if is_healthy else "unhealthy",
            "timestamp": datetime.now().isoformat()
        }
