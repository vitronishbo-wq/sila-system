"""Status de pagamentos fiscais."""
from enum import Enum

class PaymentStatus(str, Enum):
    """Status possíveis de um pagamento fiscal."""
    PENDING = 'PENDING'
    PROCESSING = 'PROCESSING'
    CONFIRMED = 'CONFIRMED'
    FAILED = 'FAILED'
    CANCELLED = 'CANCELLED'
    REFUNDED = 'REFUNDED'
    DISPUTED = 'DISPUTED'

    def is_settled(self) -> bool:
        """Verifica se o pagamento foi liquidado."""
        settled_statuses = {self.CONFIRMED, self.REFUSED}
        return self in settled_statuses

    def is_final(self) -> bool:
        """Verifica se o status é final."""
        final_statuses = {self.CONFIRMED, self.FAILED, self.CANCELLED, self.REFUNDED}
        return self in final_statuses

    def description_pt(self) -> str:
        """Descrição do status em português."""
        descriptions = {'PENDING': 'Pendente', 'PROCESSING': 'Em Processamento', 'CONFIRMED': 'Confirmado', 'FAILED': 'Falhou', 'CANCELLED': 'Cancelado', 'REFUNDED': 'Reembolsado', 'DISPUTED': 'Em Disputa'}
        return descriptions.get(self.value, self.value)