"""
Gravador imutável de auditoria para o módulo Citizen.
Persiste eventos de validação em financial_audit_logs ou fuc_events
conforme o contexto da operação.
"""
import logging
from typing import Any, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.events import CitizenValidated, CitizenValidationFailed

logger = logging.getLogger(__name__)


class ImmutableAuditWriter:
    """
    Gravador imutável: uma vez escrito, o registo de auditoria não pode ser
    alterado nem apagado. Segue o princípio de append-only para conformidade legal.
    """

    def __init__(self, db: Optional[AsyncSession] = None, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.db = db

    async def record_validation_success(self, event: CitizenValidated) -> None:
        """Persiste evento de validação bem-sucedida."""
        logger.info(
            f"AUDIT_CITIZEN: Validação aprovada para cidadão {event.citizen_id} "
            f"(status={event.status}, event_id={event.event_id})"
        )
        if self.db:
            await self._persist_audit_entry(
                entity_type="CITIZEN",
                entity_id=event.citizen_id,
                action="VALIDATION_SUCCESS",
                new_state={"status": event.status},
                performed_by="SYSTEM_FUC_VALIDATOR",
            )

    async def record_validation_failure(self, event: CitizenValidationFailed) -> None:
        """Persiste evento de falha na validação."""
        logger.warning(
            f"AUDIT_CITIZEN: Validação REJEITADA para cidadão {event.citizen_id} "
            f"(reason={event.reason}, event_id={event.event_id})"
        )
        if self.db:
            await self._persist_audit_entry(
                entity_type="CITIZEN",
                entity_id=event.citizen_id,
                action="VALIDATION_FAILED",
                previous_state=event.details,
                new_state={"reason": event.reason},
                performed_by="SYSTEM_FUC_VALIDATOR",
            )

    async def _persist_audit_entry(
        self,
        entity_type: str,
        entity_id: str,
        action: str,
        new_state: Dict[str, Any],
        performed_by: str,
        previous_state: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Grava entrada imutável na tabela financial_audit_logs."""
        from app.modules.financas.domain.models.audit_log import FinancialAudit

        entry = FinancialAudit(
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            previous_state=previous_state,
            new_state=new_state,
            performed_by=performed_by,
        )
        self.db.add(entry)
        await self.db.commit()
        logger.debug(f"AUDIT_PERSIST: {entity_type}:{entity_id}:{action} gravado.")
