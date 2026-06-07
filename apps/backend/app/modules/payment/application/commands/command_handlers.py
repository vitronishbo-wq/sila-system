"""Payment command handlers."""

from apps.backend.app.modules.payment.application.commands.payment_commands import (
    CreatePaymentCommand,
    ProcessWebhookCommand,
    RefundPaymentCommand,
    UpdatePaymentStatusCommand,
)
from ...domain.models.payment import Payment
from ...domain.ports.payment_provider_port import PaymentProviderPort
from apps.backend.app.modules.payment.domain.ports.payment_repository_port import (
    PaymentRepositoryPort,
)


class CreatePaymentHandler:
    """Handle payment creation command."""

    def __init__(self, repository: PaymentRepositoryPort, provider: PaymentProviderPort):
        self.repository = repository
        self.provider = provider

    async def handle(self, command: CreatePaymentCommand) -> Payment:
        """Execute payment creation."""
        payment = Payment(
            id=None,
            citizen_id=command.citizen_id,
            reference=command.reference,
            amount=command.amount,
            method=command.method,
            status="PENDING",
            description=command.description or "",
            metadata=command.metadata or {},
        )
        auth_result = await self.provider.authorize(payment)
        payment.provider_reference = auth_result.get("provider_reference")
        saved_payment = await self.repository.create(payment)
        return saved_payment


class RefundPaymentHandler:
    """Handle payment refund command."""

    def __init__(self, repository: PaymentRepositoryPort, provider: PaymentProviderPort):
        self.repository = repository
        self.provider = provider

    async def handle(self, command: RefundPaymentCommand) -> Payment:
        """Execute payment refund."""
        payment = await self.repository.get_by_id(command.payment_id)
        if not payment:
            raise ValueError(f"Payment {command.payment_id} not found")
        refund_result = await self.provider.refund(
            payment.provider_reference, command.amount or payment.amount
        )
        payment.status = "REFUNDED"
        payment.metadata["refund_id"] = refund_result.get("refund_id")
        await self.repository.save(payment)
        return payment


class ProcessWebhookHandler:
    """Handle webhook processing command."""

    def __init__(self, repository: PaymentRepositoryPort, provider: PaymentProviderPort):
        self.repository = repository
        self.provider = provider

    async def handle(self, command: ProcessWebhookCommand) -> Payment | None:
        """Execute webhook processing."""
        if command.signature:
            payload_str = str(command.payload)
            is_valid = await self.provider.verify_webhook(command.signature, payload_str)
            if not is_valid:
                raise ValueError("Invalid webhook signature")
        parsed = await self.provider.parse_webhook(command.payload)
        payment = await self.repository.get_by_reference(parsed.get("provider_reference"))
        if not payment:
            return None
        payment.status = parsed.get("status", payment.status)
        await self.repository.save(payment)
        return payment


class UpdatePaymentStatusHandler:
    """Handle payment status update command."""

    def __init__(self, repository: PaymentRepositoryPort):
        self.repository = repository

    async def handle(self, command: UpdatePaymentStatusCommand) -> Payment:
        """Execute payment status update."""
        payment = await self.repository.get_by_id(command.payment_id)
        if not payment:
            raise ValueError(f"Payment {command.payment_id} not found")
        payment.status = command.status
        if command.provider_reference:
            payment.provider_reference = command.provider_reference
        if command.metadata:
            payment.metadata.update(command.metadata)
        await self.repository.save(payment)
        return payment
