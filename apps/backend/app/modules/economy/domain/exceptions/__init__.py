"""Domain exceptions"""

class DomainException(Exception):
    """Base domain exception"""

    def __init__(self, message: str, code: str='DOMAIN_ERROR'):
        self.message = message
        self.code = code
        super().__init__(f'[{code}] {message}')

class EntityNotFoundError(DomainException):
    """Entity not found in repository"""

    def __init__(self, entity_type: str, entity_id: str):
        super().__init__(f'{entity_type} with ID {entity_id} not found', 'ENTITY_NOT_FOUND')

class InvalidEntityError(DomainException):
    """Entity validation failed"""

    def __init__(self, message: str):
        super().__init__(message, 'INVALID_ENTITY')

class RepositoryError(DomainException):
    """Repository operation failed"""

    def __init__(self, message: str):
        super().__init__(message, 'REPOSITORY_ERROR')

class DomainValidationError(DomainException):
    """Domain validation failed"""

    def __init__(self, message: str):
        super().__init__(message, 'DOMAIN_VALIDATION')

class InvoiceNotFoundError(DomainException):
    """Invoice not found"""

    def __init__(self, invoice_id: str):
        super().__init__(f'Invoice {invoice_id} not found', 'INVOICE_NOT_FOUND')
        self.invoice_id = invoice_id

class DuplicatePaymentError(DomainException):
    """Duplicate payment detected"""

    def __init__(self, gateway_reference: str):
        super().__init__(f'Payment with reference {gateway_reference} already exists', 'PAYMENT_DUPLICATE')
        self.gateway_reference = gateway_reference

class InvalidInvoiceStateError(DomainException):
    """Invalid invoice state transition"""

    def __init__(self, current_status: str, action: str):
        super().__init__(f'Cannot {action} when invoice is {current_status}', 'INVOICE_INVALID_STATE')
        self.current_status = current_status
        self.action = action

class FUCError(DomainException):
    """FUC integration error"""

    def __init__(self, message: str):
        super().__init__(message, 'FUC_ERROR')

__all__ = [
    'DomainException',
    'EntityNotFoundError',
    'InvalidEntityError',
    'RepositoryError',
    'DomainValidationError',
    'InvoiceNotFoundError',
    'DuplicatePaymentError',
    'InvalidInvoiceStateError',
    'FUCError',
]
