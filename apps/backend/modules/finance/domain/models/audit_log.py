from datetime import datetime, timezone
from typing import Optional, Dict, Any
from dataclasses import dataclass, field

@dataclass(frozen=True)
class FinancialAudit:
    """
    Entidade de Domínio representando um registo de auditoria imutável.
    LIVRE DE DEPENDÊNCIAS DE ORM.
    """
    entity_type: str  # 'INVOICE' ou 'PAYMENT'
    entity_id: str
    action: str
    performed_by: str
    previous_state: Optional[Dict[str, Any]] = None
    new_state: Optional[Dict[str, Any]] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    ip_address: Optional[str] = None
    id: Optional[int] = None # Definido apenas após persistência se for auto-incremento, ou UUID se preferir

    def __post_init__(self):
        # Auditoria deve ter estados se for uma alteração
        if not self.entity_id or not self.action:
            raise ValueError("Auditoria deve conter Entity ID e Action.")