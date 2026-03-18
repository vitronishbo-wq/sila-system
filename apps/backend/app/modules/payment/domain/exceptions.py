"""Exceções específicas do domínio de Pagamentos."""
import logging

logger = logging.getLogger(__name__)


class PaymentDomainException(Exception):
    """Exceção base para o domínio de Pagamentos."""
    pass


class DuplicatePaymentError(PaymentDomainException):
    """Levantada quando tentam registar um pagamento com gateway_reference duplicado."""
    
    def __init__(self, gateway_reference: str):
        self.gateway_reference = gateway_reference
        msg = (
            f"Pagamento com referência '{gateway_reference}' já existe. "
            "Idempotência garantida - rejeição de duplicata."
        )
        logger.warning(f"DuplicatePaymentError: {msg}")
        super().__init__(msg)


class InvoiceNotFoundError(PaymentDomainException):
    """Levantada quando a fatura associada ao pagamento não existe."""
    
    def __init__(self, invoice_id: str):
        self.invoice_id = invoice_id
        msg = f"Fatura '{invoice_id}' não encontrada no sistema."
        logger.error(f"InvoiceNotFoundError: {msg}")
        super().__init__(msg)


class InvalidInvoiceStateError(PaymentDomainException):
    """Levantada quando a fatura não está num estado válido para pagamento."""
    
    def __init__(self, current_status: str, action: str):
        self.current_status = current_status
        self.action = action
        msg = (
            f"Não é possível {action} com fatura em estado '{current_status}'. "
            "Estados válidos: PENDING, OVERDUE"
        )
        logger.error(f"InvalidInvoiceStateError: {msg}")
        super().__init__(msg)


class DomainValidationError(PaymentDomainException):
    """Levantada quando há violação de regra de negócio no domínio."""
    
    def __init__(self, message: str):
        msg = f"Violação de regra de domínio: {message}"
        logger.error(f"DomainValidationError: {msg}")
        super().__init__(msg)


class PaymentReconciliationError(PaymentDomainException):
    """Levantada quando há falha na reconciliação bancária."""
    
    def __init__(self, message: str, payment_id: str = None):
        self.payment_id = payment_id
        detail = f" (Pagamento: {payment_id})" if payment_id else ""
        msg = f"Falha na reconciliação: {message}{detail}"
        logger.error(f"PaymentReconciliationError: {msg}")
        super().__init__(msg)
