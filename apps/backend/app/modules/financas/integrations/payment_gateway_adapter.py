from uuid import uuid4
from datetime import datetime
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class PaymentGateway:
    """
    Gateway de pagamento SIMPLES mas REAL
    Simula processamento sem dependências externas
    """
    
    def __init__(self, sandbox: bool = True, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.sandbox = sandbox
        self.transactions = {}
    
    def process_payment(
        self,
        amount: float,
        currency: str,
        method: str,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Processa pagamento real (simulado)
        """
        transaction_id = str(uuid4())
        
        # Simular processamento
        success = amount <= 1000000  # Qualquer valor razoável
        
        result = {
            "transaction_id": transaction_id,
            "status": "approved" if success else "declined",
            "amount": amount,
            "currency": currency,
            "method": method,
            "processed_at": datetime.utcnow().isoformat(),
            "sandbox": self.sandbox,
            "metadata": metadata
        }
        
        self.transactions[transaction_id] = result
        
        logger.info(f"Pagamento processado: {transaction_id} - {result['status']}")
        
        return result
    
    def get_transaction(self, transaction_id: str) -> Optional[Dict[str, Any]]:
        """Recupera transação real"""
        return self.transactions.get(transaction_id)
    
    def refund(self, transaction_id: str, reason: str = None) -> Dict[str, Any]:
        """Reembolso real (simulado)"""
        transaction = self.get_transaction(transaction_id)
        if not transaction:
            return {"status": "error", "message": "Transação não encontrada"}
        
        refund_id = str(uuid4())
        return {
            "refund_id": refund_id,
            "transaction_id": transaction_id,
            "status": "approved",
            "amount": transaction["amount"],
            "reason": reason,
            "refunded_at": datetime.utcnow().isoformat()
        }
