from typing import Optional, List, Tuple
from uuid import UUID
from datetime import datetime
import logging

from ...domain.entities.taxpayer import Taxpayer
from ...domain.value_objects.nif import NIF
from ..ports.taxpayer_repository_port import TaxpayerRepositoryPort
from ..ports.agt_integration_port import AGTIntegrationPort
from ..ports.notification_port import NotificationPort
from ..ports.audit_port import AuditPort
from ..ports.cache_port import CachePort


class TaxpayerService:
    """Serviço principal de contribuintes"""
    
    def __init__(
        self,
        taxpayer_repo: TaxpayerRepositoryPort,
        agt_client: AGTIntegrationPort,
        notification: NotificationPort,
        audit: AuditPort,
        cache: CachePort
    ):
        self.repo = taxpayer_repo
        self.agt = agt_client
        self.notification = notification
        self.audit = audit
        self.cache = cache
        self.logger = logging.getLogger(__name__)
    
    async def register_taxpayer(
        self,
        nif: str,
        name: str,
        email: Optional[str],
        phone: Optional[str],
        address: Optional[str],
        tax_regime: str,
        registered_by: UUID,
        ip_address: Optional[str] = None
    ) -> Taxpayer:
        """Regista um novo contribuinte"""
        self.logger.info(f"Registando contribuinte NIF: {nif}")
        
        try:
            nif_obj = NIF(nif)
        except ValueError:
            self.logger.error(f"NIF inválido: {nif}")
            raise ValueError(f"NIF inválido: {nif}")
        
        existing = await self.repo.find_by_nif(nif)
        if existing:
            raise ValueError(f"Contribuinte com NIF {nif} já existe")
        
        is_valid = await self.agt.validate_nif(nif)
        if not is_valid:
            raise ValueError(f"NIF {nif} não é válido na AGT")
        
        agt_data = await self.agt.get_taxpayer_data(nif)
        if agt_data:
            name = agt_data.get('name', name)
            email = email or agt_data.get('email')
            phone = phone or agt_data.get('phone')
            address = address or agt_data.get('address')
        
        taxpayer = Taxpayer(
            nif=nif,
            name=name,
            email=email,
            phone=phone,
            address=address,
            tax_regime=tax_regime,
            registered_by=registered_by
        )
        
        saved = await self.repo.save(taxpayer)
        self.logger.info(f"Contribuinte registado com ID: {saved.id}")
        
        await self.cache.delete(f"taxpayer:nif:{nif}")
        
        await self.notification.notify_admin(
            "Novo Contribuinte Registado",
            f"Contribuinte {saved.name} (NIF: {saved.nif}) foi registado com sucesso",
            {"taxpayer_id": str(saved.id)}
        )
        
        await self.audit.log(
            action="TAXPAYER_REGISTERED",
            user_id=registered_by,
            entity_id=saved.id,
            entity_type="taxpayer",
            details={"nif": nif, "name": name, "tax_regime": tax_regime},
            ip_address=ip_address
        )
        
        return saved
    
    async def get_taxpayer(self, taxpayer_id: UUID) -> Optional[Taxpayer]:
        """Busca contribuinte por ID (com cache)"""
        cache_key = f"taxpayer:id:{taxpayer_id}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached
        
        taxpayer = await self.repo.find_by_id(taxpayer_id)
        if taxpayer:
            await self.cache.set(cache_key, taxpayer, ttl=300)
        return taxpayer
    
    async def get_taxpayer_by_nif(self, nif: str) -> Optional[Taxpayer]:
        """Busca contribuinte por NIF (com cache)"""
        cache_key = f"taxpayer:nif:{nif}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached
        
        taxpayer = await self.repo.find_by_nif(nif)
        if taxpayer:
            await self.cache.set(cache_key, taxpayer, ttl=300)
        return taxpayer
    
    async def update_taxpayer(
        self,
        taxpayer_id: UUID,
        updates: dict,
        updated_by: UUID,
        ip_address: Optional[str] = None
    ) -> Taxpayer:
        """Atualiza dados do contribuinte"""
        taxpayer = await self.repo.find_by_id(taxpayer_id)
        if not taxpayer:
            raise ValueError("Contribuinte não encontrado")
        
        old_values = {
            "name": taxpayer.name,
            "email": taxpayer.email,
            "phone": taxpayer.phone,
            "address": taxpayer.address,
            "tax_regime": taxpayer.tax_regime,
            "status": taxpayer.status
        }
        
        changes = {}
        for key, value in updates.items():
            if hasattr(taxpayer, key) and value is not None:
                old_value = getattr(taxpayer, key)
                if old_value != value:
                    setattr(taxpayer, key, value)
                    changes[key] = {"old": old_value, "new": value}
        
        if not changes:
            return taxpayer
        
        taxpayer.updated_at = datetime.now()
        taxpayer.updated_by = updated_by
        
        saved = await self.repo.save(taxpayer)
        
        await self.cache.delete(f"taxpayer:id:{taxpayer_id}")
        await self.cache.delete(f"taxpayer:nif:{taxpayer.nif}")
        
        await self.audit.log(
            action="TAXPAYER_UPDATED",
            user_id=updated_by,
            entity_id=taxpayer_id,
            entity_type="taxpayer",
            details={"changes": changes, "old_values": old_values},
            ip_address=ip_address
        )
        
        return saved
    
    async def change_status(
        self,
        taxpayer_id: UUID,
        new_status: str,
        reason: str,
        changed_by: UUID,
        ip_address: Optional[str] = None
    ) -> Taxpayer:
        """Altera status do contribuinte"""
        taxpayer = await self.repo.find_by_id(taxpayer_id)
        if not taxpayer:
            raise ValueError("Contribuinte não encontrado")
        
        old_status = taxpayer.status
        if old_status == new_status:
            return taxpayer
        
        taxpayer.status = new_status
        taxpayer.updated_at = datetime.now()
        taxpayer.updated_by = changed_by
        
        saved = await self.repo.save(taxpayer)
        
        await self.cache.delete(f"taxpayer:id:{taxpayer_id}")
        await self.cache.delete(f"taxpayer:nif:{taxpayer.nif}")
        
        await self.notification.notify_taxpayer(
            taxpayer_id,
            "Status Fiscal Alterado",
            f"Seu status fiscal foi alterado de {old_status} para {new_status}",
            {"reason": reason}
        )
        
        await self.audit.log(
            action="TAXPAYER_STATUS_CHANGED",
            user_id=changed_by,
            entity_id=taxpayer_id,
            entity_type="taxpayer",
            details={"old_status": old_status, "new_status": new_status, "reason": reason},
            ip_address=ip_address
        )
        
        return saved
    
    async def list_taxpayers(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        tax_regime: Optional[str] = None,
        search: Optional[str] = None
    ) -> Tuple[List[Taxpayer], int]:
        """Lista contribuintes com filtros"""
        filters = {}
        if status:
            filters["status"] = status
        if tax_regime:
            filters["tax_regime"] = tax_regime
        if search:
            filters["search"] = search
        
        return await self.repo.list_all(skip, limit, filters)
