"""
Domain-level exceptions for Economy::Core module.
Consolidated from former treasury and financas subdomains.
"""


class FinancasError(Exception):
    """Base exception for all Financas/Economy errors."""
    pass


class DomainValidationError(FinancasError):
    """Raised when a domain validation rule is violated."""
    pass


class InvalidInvoiceStateError(FinancasError):
    """Raised when an invoice state transition is invalid."""
    def __init__(self, current_status: str, action: str):
        self.current_status = current_status
        self.action = action
        super().__init__(
            f"Cannot {action} when invoice is in status: {current_status}"
        )


class InvoiceNotFoundError(FinancasError):
    """Raised when an invoice cannot be found by ID."""
    def __init__(self, invoice_id: str):
        self.invoice_id = invoice_id
        super().__init__(f"Invoice not found: {invoice_id}")


class DuplicatePaymentError(FinancasError):
    """Raised when a payment with the same gateway reference already exists."""
    def __init__(self, gateway_reference: str):
        self.gateway_reference = gateway_reference
        super().__init__(
            f"Payment with reference already exists: {gateway_reference}"
        )


class FUCError(FinancasError):
    """Raised when Ficheiro Único do Cidadão (FUC) service is unavailable."""
    pass


class TaxLedgerError(FinancasError):
    """Raised when tax ledger operations fail."""
    pass


class TreasuryAccountError(FinancasError):
    """Raised when treasury account operations fail."""
    pass