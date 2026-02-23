"""
Audit Handlers — Processamento de eventos citizen → registos de auditoria financeira.
Integração cross-module: citizen events disparam registos imutáveis no financial_audit_logs.
"""
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.events import CitizenValidationFailed
from app.modules.financas.domain.models.audit_log import FinancialAudit

logger = logging.getLogger(__name__)


async def handle_citizen_validation_failed(
    event: CitizenValidationFailed,
    db_session: AsyncSession,
) -> None:
    """
    Handler para eventos CitizenValidationFailed.
    Grava um registo imutável na tabela financial_audit_logs
    quando a validação FUC é rejeitada durante operações financeiras.
    """
    from app.modules.financas.infrastructure.repositories.audit_repository import FinancialAuditRepository
    
    repo = FinancialAuditRepository(db_session)
    log_entry = FinancialAudit(
        entity_type="CITIZEN",
        entity_id=event.citizen_id,
        action="INVOICE_CREATION_FAILED",
        previous_state=event.details,
        new_state={"reason": event.reason},
        performed_by="SYSTEM_FUC_VALIDATOR",
    )
    await repo.create(log_entry)
    await db_session.commit()

    logger.info(
        f"AUDIT_HANDLER: Registado INVOICE_CREATION_FAILED para cidadão {event.citizen_id} "
        f"(reason={event.reason})"
    )
