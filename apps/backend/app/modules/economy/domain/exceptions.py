from __future__ import annotations


class EconomyError(Exception):
    pass


class DomainValidationError(EconomyError):
    pass


class FUCError(EconomyError):
    pass


class InvoiceNotFoundError(EconomyError):
    pass


class InvalidInvoiceStateError(EconomyError):
    pass


class DuplicatePaymentError(EconomyError):
    pass
