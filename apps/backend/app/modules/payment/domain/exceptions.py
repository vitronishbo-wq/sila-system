"""Exceções mínimas do domínio de pagamentos."""


class DomainValidationError(ValueError):
    """Base para violações de regra de negócio em pagamentos."""


class DuplicatePaymentError(DomainValidationError):
    """Pagamento duplicado para a mesma referência de gateway."""

    def __init__(self, gateway_reference: str):
        self.gateway_reference = gateway_reference
        super().__init__(f"Payment with gateway reference '{gateway_reference}' already exists")


class InvoiceNotFoundError(DomainValidationError):
    """Fatura não encontrada."""

    def __init__(self, invoice_id: str):
        self.invoice_id = invoice_id
        super().__init__(f"Invoice '{invoice_id}' not found")


class InvalidInvoiceStateError(DomainValidationError):
    """Estado da fatura incompatível com a operação."""

    def __init__(self, current_status: str, action: str):
        self.current_status = current_status
        self.action = action
        super().__init__(f"Cannot {action} when invoice status is '{current_status}'")


__all__ = [
    "DomainValidationError",
    "DuplicatePaymentError",
    "InvalidInvoiceStateError",
    "InvoiceNotFoundError",
]
