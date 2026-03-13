from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List
import uuid

class RequestStatus(Enum):
    """Workflow administrativo para serviços de identidade."""
    PENDING = 'PENDING'
    PENDING_FUC_VALIDATION = 'PENDING_FUC_VALIDATION'
    FUC_VALIDATION = 'FUC_VALIDATION'
    APPROVED = 'APPROVED'
    PRINTING = 'PRINTING'
    COMPLETED = 'COMPLETED'
    REJECTED = 'REJECTED'
    CANCELLED = 'CANCELLED'

@dataclass
class IdentityRequest:
    """
    Orquestrador de serviço (Process Object).
    Gerencia o ciclo de vida de uma solicitação (001, 002, 003, etc).
    """
    citizen_fuc_id: str
    service_code: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    status: RequestStatus = RequestStatus.PENDING
    bi_id: Optional[uuid.UUID] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    notes: List[str] = field(default_factory=list)

    def transition_to(self, new_status: RequestStatus, reason: Optional[str]=None):
        """Transição formal de estado com registro de motivo."""
        self.status = new_status
        self.updated_at = datetime.utcnow()
        if reason:
            self.add_note('SYSTEM', f'Transition to {new_status.name}: {reason}')

    def update_status(self, new_status: RequestStatus):
        """Alias para conformidade com serviços legados no módulo."""
        self.transition_to(new_status)

    def add_note(self, operator: str, text: str):
        """Adiciona uma entrada ao log administrativo do processo."""
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        self.notes.append(f'[{timestamp}] {operator}: {text}')
        self.updated_at = datetime.utcnow()

    def complete(self, bi_id: uuid.UUID):
        """Finaliza o processo vinculando o documento gerado."""
        self.bi_id = bi_id
        self.transition_to(RequestStatus.COMPLETED, 'Processo finalizado com sucesso.')