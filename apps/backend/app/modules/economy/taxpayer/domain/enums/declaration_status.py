"""Status de declarações fiscais."""
from enum import Enum

class DeclarationStatus(str, Enum):
    """Status possíveis de uma declaração fiscal."""
    DRAFT = 'DRAFT'
    SUBMITTED = 'SUBMITTED'
    RECEIVED = 'RECEIVED'
    PROCESSING = 'PROCESSING'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    AMENDED = 'AMENDED'
    CANCELLED = 'CANCELLED'
    ARCHIVED = 'ARCHIVED'

    def is_terminal(self) -> bool:
        """Verifica se o status é terminal."""
        terminal_statuses = {self.ACCEPTED, self.REJECTED, self.CANCELLED, self.ARCHIVED}
        return self in terminal_statuses

    def is_pending(self) -> bool:
        """Verifica se a declaração está pendente de resposta da AGT."""
        pending_statuses = {self.SUBMITTED, self.RECEIVED, self.PROCESSING}
        return self in pending_statuses

    def description_pt(self) -> str:
        """Descrição do status em português."""
        descriptions = {'DRAFT': 'Rascunho', 'SUBMITTED': 'Submetida', 'RECEIVED': 'Recebida', 'PROCESSING': 'Em Processamento', 'ACCEPTED': 'Aceite', 'REJECTED': 'Rejeitada', 'AMENDED': 'Alterada', 'CANCELLED': 'Cancelada', 'ARCHIVED': 'Arquivada'}
        return descriptions.get(self.value, self.value)