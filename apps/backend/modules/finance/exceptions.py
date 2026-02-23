"""Exceções específicas do módulo de Finanças.

Todas as exceções herdam de FinanceError (base) com codes padronizados para
facilitação de tratamento e logging centralizado.
"""
from typing import Any, Dict, Optional


class FinanceError(Exception):
    """Exceção base para o módulo de finanças."""
    def __init__(self, message: str, code: str = "FINANCE_ERROR", **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.message = message
        self.code = code
        super().__init__(self.message)


class InvoiceError(FinanceError):
    """Erros relacionados a faturas."""
    pass


class InvoiceNotFoundError(InvoiceError):
    def __init__(self, invoice_id: str, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        super().__init__(
            message=f"Fatura com ID {invoice_id} não encontrada.",
            code="INVOICE_NOT_FOUND"
        )


class InvalidInvoiceStateError(InvoiceError):
    def __init__(self, current_status: str, action: str, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        super().__init__(
            message=f"Não é possível {action} uma fatura no estado {current_status}.",
            code="INVALID_INVOICE_STATE"
        )


class InvoiceCreationError(InvoiceError):
    """Lançada quando não é possível criar uma fatura."""
    def __init__(self, citizen_id: str, reason: str, details: Optional[Dict[str, Any]] = None, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.citizen_id = citizen_id
        self.reason = reason
        self.details = details or {}
        message = f"Não foi possível criar fatura para cidadão '{citizen_id}': {reason}"
        super().__init__(message=message, code="INVOICE_CREATION_FAILED")


class PaymentError(FinanceError):
    """Erros relacionados a pagamentos."""
    pass


class DuplicatePaymentError(PaymentError):
    def __init__(self, reference: str, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        super().__init__(
            message=f"Já existe um pagamento processado para a referência {reference}.",
            code="DUPLICATE_PAYMENT"
        )


class PaymentGatewayError(PaymentError):
    def __init__(self, provider: str, details: str, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        super().__init__(
            message=f"Falha na comunicação com o gateway {provider}: {details}",
            code="GATEWAY_COMMUNICATION_FAILURE"
        )


class PaymentProcessingError(PaymentError):
    """Lançada quando o processamento de um pagamento falha."""
    def __init__(self, payment_id: str, reason: str, processor_response: Optional[Dict[str, Any]] = None, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.payment_id = payment_id
        self.reason = reason
        self.processor_response = processor_response or {}
        message = f"Erro ao processar pagamento '{payment_id}': {reason}"
        super().__init__(message=message, code="PAYMENT_PROCESSING_FAILED")


class PaymentIdempotencyError(PaymentError):
    """Lançada quando tenta-se processar o mesmo pagamento duas vezes."""
    def __init__(self, payment_id: str, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.payment_id = payment_id
        message = f"Pagamento '{payment_id}' já foi processado anteriormente"
        super().__init__(message=message, code="PAYMENT_IDEMPOTENCY_VIOLATION")


class DomainValidationError(FinanceError):
    """Exceção lançada quando uma regra de negócio do domínio é violada."""
    def __init__(self, message: str, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        super().__init__(message=message, code="DOMAIN_VALIDATION_ERROR")


class FUCError(FinanceError):
    """Erro na integração com o Ficheiro Único do Cidadão."""
    def __init__(self, message: str, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        super().__init__(message=message, code="FUC_INTEGRATION_ERROR")


class InvalidCitizenError(FUCError):
    """Lançada quando o cidadão é inválido ou não está ativo no FUC."""
    def __init__(self, citizen_id: str, reason: str = "Cidadão inválido ou inativo", **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.citizen_id = citizen_id
        self.reason = reason
        message = f"Cidadão '{citizen_id}' inválido: {reason}"
        super().__init__(message)


class AuditLogError(FinanceError):
    """Lançada quando há erro ao gravar auditoria."""
    def __init__(self, operation: str, reason: str, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.operation = operation
        self.reason = reason
        message = f"Erro ao gravar auditoria para operação '{operation}': {reason}"
        super().__init__(message=message, code="AUDIT_LOG_ERROR")
