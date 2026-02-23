"""Status de declarações fiscais."""
from enum import Enum


class DeclarationStatus(str, Enum):
    """Status possíveis de uma declaração fiscal."""
    
    DRAFT = "DRAFT"  # Rascunho - em elaboração
    SUBMITTED = "SUBMITTED"  # Submetida à AGT
    RECEIVED = "RECEIVED"  # Recebida pela AGT
    PROCESSING = "PROCESSING"  # Em processamento na AGT
    ACCEPTED = "ACCEPTED"  # Aceite pela AGT
    REJECTED = "REJECTED"  # Rejeitada pela AGT
    AMENDED = "AMENDED"  # Alterada/Retificada
    CANCELLED = "CANCELLED"  # Cancelada
    ARCHIVED = "ARCHIVED"  # Arquivada

    def is_terminal(self) -> bool:
        """Verifica se o status é terminal."""
        terminal_statuses = {
            self.ACCEPTED,
            self.REJECTED,
            self.CANCELLED,
            self.ARCHIVED,
        }
        return self in terminal_statuses

    def is_pending(self) -> bool:
        """Verifica se a declaração está pendente de resposta da AGT."""
        pending_statuses = {
            self.SUBMITTED,
            self.RECEIVED,
            self.PROCESSING,
        }
        return self in pending_statuses

    def description_pt(self) -> str:
        """Descrição do status em português."""
        descriptions = {
            "DRAFT": "Rascunho",
            "SUBMITTED": "Submetida",
            "RECEIVED": "Recebida",
            "PROCESSING": "Em Processamento",
            "ACCEPTED": "Aceite",
            "REJECTED": "Rejeitada",
            "AMENDED": "Alterada",
            "CANCELLED": "Cancelada",
            "ARCHIVED": "Arquivada",
        }
        return descriptions.get(self.value, self.value)
