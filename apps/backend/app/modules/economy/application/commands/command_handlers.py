"""Economy command handlers."""
from datetime import datetime
from apps.backend.app.modules.economy.application.commands.economy_commands import CreateInvoiceCommand, ProcessInvoiceCommand, CreatePaymentCommand
from apps.backend.app.modules.economy.domain.models.invoice import Invoice
from apps.backend.app.modules.economy.domain.models.payment import Payment
from apps.backend.app.modules.economy.domain.models.enums import InvoiceStatus, PaymentStatus
from apps.backend.app.modules.economy.domain.ports.invoice_repository_port import InvoiceRepositoryPort
from apps.backend.app.modules.economy.domain.ports.payment_repository_port import PaymentRepositoryPort
import uuid

class CreateInvoiceHandler:
    """Handle invoice creation command."""

    def __init__(self, invoice_repo: InvoiceRepositoryPort):
        self.invoice_repo = invoice_repo

    async def handle(self, command: CreateInvoiceCommand) -> Invoice:
        """Execute invoice creation."""
        invoice = Invoice(id=str(uuid.uuid4()), citizen_id=command.citizen_id, reference=command.reference, revenue_code=command.metadata.get('revenue_code', '0000') if command.metadata else '0000', cost_center=command.metadata.get('cost_center', 'CC0001') if command.metadata else 'CC0001', service_code=command.metadata.get('service_code', 'SRV0001') if command.metadata else 'SRV0001', service_name=command.metadata.get('service_name', 'Serviço') if command.metadata else 'Serviço', amount=float(command.amount), due_date=command.metadata.get('due_date', datetime.utcnow()) if command.metadata else datetime.utcnow(), currency=command.metadata.get('currency', 'AOA') if command.metadata else 'AOA', status=InvoiceStatus.PENDING, description=command.description or '')
        saved_invoice = await self.invoice_repo.create(invoice)
        return saved_invoice

class ProcessInvoiceHandler:
    """Handle invoice processing command."""

    def __init__(self, invoice_repo: InvoiceRepositoryPort):
        self.invoice_repo = invoice_repo

    async def handle(self, command: ProcessInvoiceCommand) -> Invoice:
        """Execute invoice processing."""
        invoice = await self.invoice_repo.get_by_id(command.invoice_id)
        if not invoice:
            raise ValueError(f'Invoice {command.invoice_id} not found')
        new_status = InvoiceStatus(command.status)
        audit_data = invoice.change_status(new_status, command.metadata.get('reason', '') if command.metadata else '')
        if command.metadata:
            if hasattr(invoice, 'metadata'):
                invoice.metadata.update(command.metadata)
        await self.invoice_repo.save(invoice)
        return invoice

class CreatePaymentHandler:
    """Handle payment creation command."""

    def __init__(self, payment_repo: PaymentRepositoryPort, invoice_repo: InvoiceRepositoryPort):
        self.payment_repo = payment_repo
        self.invoice_repo = invoice_repo

    async def handle(self, command: CreatePaymentCommand) -> Payment:
        """Execute payment creation."""
        invoice = await self.invoice_repo.get_by_id(command.invoice_id)
        if not invoice:
            raise ValueError(f'Invoice {command.invoice_id} not found')
        if command.amount > invoice.amount:
            raise ValueError(f'Payment amount {command.amount} exceeds invoice amount {invoice.amount}')
        payment = Payment(id=str(uuid.uuid4()), invoice_id=command.invoice_id, citizen_id=invoice.citizen_id, amount=float(command.amount), gateway_reference=command.reference or str(uuid.uuid4()), payment_method=command.method, currency=command.metadata.get('currency', 'AOA') if command.metadata else 'AOA', status=PaymentStatus.PENDING)
        saved_payment = await self.payment_repo.create(payment)
        total_paid = sum([p.amount for p in await self.payment_repo.list_by_invoice(invoice.id)])
        if total_paid >= invoice.amount:
            invoice.status = InvoiceStatus.PAID
            invoice.paid_at = datetime.utcnow()
            await self.invoice_repo.save(invoice)
        return saved_payment