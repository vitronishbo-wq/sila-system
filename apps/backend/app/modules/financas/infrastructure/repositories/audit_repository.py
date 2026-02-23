from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from ...domain.models.audit_log import FinancialAudit
from ..models.audit_log_model import FinancialAuditModel

class FinancialAuditRepository:
    """Repositório de auditoria financeira com mapeamento entre Domínio e Persistência."""
    
    def __init__(self, db: AsyncSession, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.db = db

    def _to_domain(self, model: FinancialAuditModel) -> FinancialAudit:
        """Converte modelo de persistência para entidade de domínio."""
        return FinancialAudit(
            id=model.id,
            entity_type=model.entity_type,
            entity_id=model.entity_id,
            action=model.action,
            performed_by=model.performed_by,
            previous_state=model.previous_state,
            new_state=model.new_state,
            timestamp=model.timestamp,
            ip_address=model.ip_address
        )

    def _to_model(self, domain: FinancialAudit) -> FinancialAuditModel:
        """Converte entidade de domínio para modelo de persistência."""
        # Note: id is usually auto-increment in DB for audit logs
        return FinancialAuditModel(
            entity_type=domain.entity_type,
            entity_id=domain.entity_id,
            action=domain.action,
            performed_by=domain.performed_by,
            previous_state=domain.previous_state,
            new_state=domain.new_state,
            timestamp=domain.timestamp,
            ip_address=domain.ip_address
        )

    async def create(self, audit: FinancialAudit) -> FinancialAudit:
        """Persiste um novo registo de auditoria."""
        model = self._to_model(audit)
        self.db.add(model)
        await self.db.flush()
        return self._to_domain(model)

    async def get_by_entity(self, entity_type: str, entity_id: str) -> List[FinancialAudit]:
        """Busca histórico de auditoria para uma entidade específica."""
        stmt = select(FinancialAuditModel).where(
            FinancialAuditModel.entity_type == entity_type,
            FinancialAuditModel.entity_id == entity_id
        ).order_by(FinancialAuditModel.timestamp.desc())
        
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def list_recent(self, limit: int = 50) -> List[FinancialAudit]:
        """Lista registos recentes de auditoria global."""
        stmt = select(FinancialAuditModel).order_by(FinancialAuditModel.timestamp.desc()).limit(limit)
        result = await self.db.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]
