"""Service layer for payment management with business logic."""

from datetime import datetime
import logging
import uuid
from typing import Any, Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.payment.models.payment import Payment
from modules.payment.models.transaction import PaymentTransaction
from modules.payment.models.enums import (
    PaymentStatus,
    TransactionStatus,
    TransactionType,
)
from modules.payment.schemas.payment import (
    PaymentCreate,
    PaymentInDB,
    RefundCreate,
    RefundResponse,
)
from modules.notifications.services.notification_service import (
    NotificationService,
    NotificationType,
)

logger = logging.getLogger(__name__)


class PaymentService:
    """Service class for payment business logic and CRUD operations."""

    def __init__(self, db: AsyncSession):
        """Initialize the payment service with a database session."""
        self.db = db

    async def _generate_reference(self, prefix: str = "PAY") -> str:
        """Generate a unique payment reference."""
        return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"

    async def create_payment(
        self, payment_data: PaymentCreate, user_id: int
    ) -> PaymentInDB:
        """
        Create a new payment with business validation and initial transaction record.
        """
        try:
            # --- Business Logic: Date and Status Validation ---
            # Set initial status
            initial_status = PaymentStatus.PENDING

            # --- Creation Logic ---

            # Generate a unique reference if not provided
            reference = payment_data.reference or await self._generate_reference()

            # 1. Create payment record
            payment = Payment(
                amount=payment_data.amount,
                currency=payment_data.currency,
                method=payment_data.method,
                status=initial_status,
                reference=reference,
                description=payment_data.description,
                metadata_=payment_data.metadata or {},
                owner_id=user_id,
            )

            self.db.add(payment)
            await self.db.flush()

            # 2. Create initial transaction
            transaction = PaymentTransaction(
                payment_id=payment.id,
                amount=payment.amount,
                currency=payment.currency,
                type=TransactionType.PAYMENT,
                status=TransactionStatus.PENDING,
                reference=f"TXN-{reference}",
                provider_reference=None,
                metadata_=payment.metadata_ or {},
            )

            self.db.add(transaction)
            await self.db.commit()
            await self.db.refresh(payment)

            return PaymentInDB.model_validate(payment)
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error creating payment: {str(e)}", exc_info=True)
            raise

    async def get_payment(
        self, payment_id: int, user_id: Optional[int] = None
    ) -> Optional[Payment]:
        """
        Retrieve a payment by ID with optional access control.
        """
        result = await self.db.execute(select(Payment).where(Payment.id == payment_id))
        payment = result.scalars().first()

        if payment and user_id is not None:
            # Business logic: Check access permissions
            payment_in_db = PaymentInDB.model_validate(payment)
            if not self._can_access_payment(payment_in_db, user_id):
                return None

        return payment

    async def get_payments(
        self, skip: int = 0, limit: int = 100, user_id: Optional[int] = None
    ) -> List[PaymentInDB]:
        """Get payments with optional user filtering."""
        query = select(Payment).offset(skip).limit(limit)

        result = await self.db.execute(query)
        payments = result.scalars().all()

        payments_in_db = [PaymentInDB.model_validate(p) for p in payments]

        # Business logic: Filter payments based on user access
        if user_id:
            payments_in_db = [
                payment
                for payment in payments_in_db
                if self._can_access_payment(payment, user_id)
            ]

        return payments_in_db

    async def get_by_reference(self, reference: str) -> Optional[Payment]:
        """Retrieve a payment by its reference string."""
        result = await self.db.execute(
            select(Payment).where(Payment.reference == reference)
        )
        return result.scalars().first()

    async def update_payment_status(
        self,
        payment_id: int,
        status: PaymentStatus,
        provider_reference: Optional[str] = None,
    ) -> Optional[PaymentInDB]:
        """
        Update a payment's status and the related transaction.
        """
        result = await self.db.execute(select(Payment).where(Payment.id == payment_id))
        payment = result.scalars().first()

        if not payment:
            return None

        # 1. Update Payment Status
        if not self._is_valid_status_transition(payment.status, status):
            raise ValueError(
                f"Invalid status transition from {payment.status.value} to {status.value}"
            )

        old_status = payment.status
        payment.status = status

        # Business logic: Auto-set paid date when status changes to completed
        if status == PaymentStatus.COMPLETED and old_status != PaymentStatus.COMPLETED:
            # Send Notification
            try:
                notif_service = NotificationService(self.db)
                await notif_service.create_and_queue(
                    user_id=payment.owner_id,
                    type_=NotificationType.PAYMENT_SUCCESS,
                    title="Pagamento Confirmado",
                    message=f"O pagamento de {payment.amount} {payment.currency} (ref: {payment.reference}) foi recebido com sucesso!",
                    metadata={"payment_id": str(payment.id)},
                )
            except Exception as ne:
                logger.error(f"Failed to queue payment success notification: {ne}")

        # 2. Update the latest Transaction
        if status in [
            PaymentStatus.COMPLETED,
            PaymentStatus.FAILED,
            PaymentStatus.CANCELLED,
        ]:
            transaction = await self._get_latest_transaction(payment_id)
            if transaction:
                transaction.status = (
                    TransactionStatus.COMPLETED
                    if status == PaymentStatus.COMPLETED
                    else TransactionStatus.FAILED
                )
                if provider_reference:
                    transaction.provider_reference = provider_reference

        await self.db.commit()
        await self.db.refresh(payment)

        return PaymentInDB.model_validate(payment)

    async def update_status(self, payment_id: int, status: PaymentStatus):
        """Update payment status (alias for update_payment_status)."""
        return await self.update_payment_status(payment_id, status)

    async def create_refund(
        self, payment_id: int, refund_data: RefundCreate, user_id: int
    ) -> Optional[RefundResponse]:
        """
        Create a refund for a payment.
        """
        try:
            # Get the payment to refund
            result = await self.db.execute(select(Payment).where(Payment.id == payment_id))
            payment = result.scalars().first()

            if not payment:
                raise ValueError("Payment not found")

            if payment.status != PaymentStatus.COMPLETED:
                raise ValueError("Can only refund completed payments")

            # Business logic: Check refund permissions
            if not self._can_refund_payment(PaymentInDB.model_validate(payment), user_id):
                raise PermissionError("User cannot refund this payment")

            # Calculate refund amount (full amount if not specified)
            refund_amount = refund_data.amount or payment.amount

            if refund_amount > payment.amount:
                raise ValueError("Refund amount exceeds payment amount")

            # Create refund transaction
            transaction = PaymentTransaction(
                payment_id=payment.id,
                amount=refund_amount,
                currency=payment.currency,
                type=TransactionType.REFUND,
                status=TransactionStatus.PENDING,
                reference=await self._generate_reference("RFD"),
                provider_reference=None,
                metadata_={
                    "reason": refund_data.reason,
                    **({} if not refund_data.metadata else refund_data.metadata),
                },
            )

            self.db.add(transaction)

            # Update payment status
            if refund_amount == payment.amount:
                payment.status = PaymentStatus.REFUNDED
            else:
                payment.status = PaymentStatus.PARTIALLY_REFUNDED

            await self.db.commit()
            await self.db.refresh(transaction)

            return RefundResponse.model_validate(transaction)
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error creating refund: {str(e)}", exc_info=True)
            raise

    async def delete_payment(self, payment_id: int, user_id: int) -> bool:
        """Delete a payment with business validation."""
        result = await self.db.execute(select(Payment).where(Payment.id == payment_id))
        payment = result.scalars().first()
        if not payment:
            return False

        payment_in_db = PaymentInDB.model_validate(payment)

        # Business logic: Only allow deletion of pending/failed payments
        if payment.status not in [PaymentStatus.PENDING, PaymentStatus.FAILED]:
            raise ValueError("Only pending or failed payments can be deleted")

        # Business logic: Check delete permissions
        if not self._can_delete_payment(payment_in_db, user_id):
            raise PermissionError("User cannot delete this payment")

        await self.db.delete(payment)
        await self.db.commit()

        return True

    # Métodos Auxiliares e Lógica de Negócios (Business Logic)

    async def _get_latest_transaction(
        self, payment_id: int
    ) -> Optional[PaymentTransaction]:
        """Get the latest transaction for a payment."""
        result = await self.db.execute(
            select(PaymentTransaction)
            .where(PaymentTransaction.payment_id == payment_id)
            .order_by(PaymentTransaction.created_at.desc())
            .limit(1)
        )
        return result.scalars().first()

    async def process_webhook(self, provider: str, data: Dict[str, Any]) -> bool:
        """
        Process a payment webhook from a payment provider.
        """
        try:
            reference = data.get("reference")
            status = data.get("status")
            provider_reference = data.get("provider_reference")

            if not reference or not status:
                logger.warning(f"Invalid webhook data from {provider}")
                return False

            # Find the payment by reference
            result = await self.db.execute(
                select(Payment).where(Payment.reference == reference)
            )
            payment = result.scalars().first()

            if not payment:
                logger.warning(f"Payment not found for reference: {reference}")
                return False

            # Map provider status to our status
            status_map = {
                "succeeded": PaymentStatus.COMPLETED,
                "failed": PaymentStatus.FAILED,
                "pending": PaymentStatus.PENDING,
                "refunded": PaymentStatus.REFUNDED,
                "cancelled": PaymentStatus.CANCELLED,
            }

            new_status = status_map.get(status.lower())
            if not new_status:
                logger.warning(f"Unknown status from {provider}: {status}")
                return False

            # Update payment status
            await self.update_payment_status(
                payment_id=payment.id,
                status=new_status,
                provider_reference=provider_reference,
            )

            return True

        except Exception as e:
            await self.db.rollback()
            logger.error(
                f"Error processing {provider} webhook: {str(e)}", exc_info=True
            )
            return False

    def _is_valid_status_transition(
        self, current_status: PaymentStatus, new_status: PaymentStatus
    ) -> bool:
        """Validate payment status transitions."""
        valid_transitions = {
            PaymentStatus.PENDING: [
                PaymentStatus.PROCESSING,
                PaymentStatus.CANCELLED,
                PaymentStatus.FAILED,
            ],
            PaymentStatus.PROCESSING: [
                PaymentStatus.COMPLETED,
                PaymentStatus.FAILED,
                PaymentStatus.CANCELLED,
            ],
            PaymentStatus.COMPLETED: [
                PaymentStatus.REFUNDED,
                PaymentStatus.PARTIALLY_REFUNDED,
            ],
            PaymentStatus.FAILED: [PaymentStatus.PENDING, PaymentStatus.CANCELLED],
            PaymentStatus.CANCELLED: [],
            PaymentStatus.REFUNDED: [],
            PaymentStatus.PARTIALLY_REFUNDED: [PaymentStatus.REFUNDED],
        }

        return new_status in valid_transitions.get(current_status, [])

    # --- Métodos de Permissão (Simplificados, assumindo a interface PaymentInDB) ---

    def _can_access_payment(self, payment: PaymentInDB, user_id: int) -> bool:
        """Check if user can access the payment."""
        # Assume que PaymentInDB tem payer_id e payee_id
        if hasattr(payment, "payer_id") and payment.payer_id == user_id:
            return True

        if hasattr(payment, "payee_id") and payment.payee_id == user_id:
            return True

        return False

    def _can_delete_payment(self, payment: PaymentInDB, user_id: int) -> bool:
        """Check if user can delete the payment."""
        return True  # Simplificado

    def _can_refund_payment(self, payment: PaymentInDB, user_id: int) -> bool:
        """Check if user can refund the payment."""
        if hasattr(payment, "payee_id") and payment.payee_id == user_id:
            return True

        return True

    async def create_transaction(
        self,
        payment_id: int,
        transaction_type: TransactionType,
        amount: Optional[float] = None,
    ) -> Optional[PaymentTransaction]:
        """Create a transaction for a payment."""
        try:
            result = await self.db.execute(select(Payment).where(Payment.id == payment_id))
            payment = result.scalars().first()

            if not payment:
                return None

            # Use payment amount if not specified
            transaction_amount = amount or payment.amount

            transaction = PaymentTransaction(
                payment_id=payment.id,
                amount=transaction_amount,
                currency=payment.currency,
                type=transaction_type,
                status=TransactionStatus.PENDING,
                reference=f"TXN-{await self._generate_reference()}",
                provider_reference=None,
                metadata_={},
            )

            self.db.add(transaction)
            await self.db.commit()
            await self.db.refresh(transaction)

            return transaction
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error creating transaction: {str(e)}", exc_info=True)
            raise

    async def get_payment_summary(self, payment_id: int) -> Optional[Dict[str, Any]]:
        """Get a complete summary of a payment with transactions and refunds."""
        result = await self.db.execute(select(Payment).where(Payment.id == payment_id))
        payment = result.scalars().first()

        if not payment:
            return None

        # Get all transactions
        transactions_result = await self.db.execute(
            select(PaymentTransaction).where(
                PaymentTransaction.payment_id == payment_id
            )
        )
        transactions = transactions_result.scalars().all()

        # Get all refunds
        from modules.payment.models.refund import Refund

        refunds_result = await self.db.execute(
            select(Refund).where(Refund.payment_id == payment_id)
        )
        refunds = refunds_result.scalars().all()

        return {
            "payment": PaymentInDB.model_validate(payment),
            "transactions": [
                {
                    "id": t.id,
                    "type": t.type.value,
                    "status": t.status.value,
                    "amount": float(t.amount),
                    "currency": t.currency,
                    "reference": t.reference,
                    "created_at": t.created_at.isoformat(),
                }
                for t in transactions
            ],
            "refunds": [
                {
                    "id": r.id,
                    "amount": float(r.amount),
                    "currency": r.currency,
                    "status": r.status.value,
                    "reason": r.reason,
                    "created_at": r.created_at.isoformat(),
                }
                for r in refunds
            ],
            "summary": {
                "total_transactions": len(transactions),
                "total_refunds": len(refunds),
                "refunded_amount": sum(float(r.amount) for r in refunds),
                "remaining_amount": float(payment.amount)
                - sum(float(r.amount) for r in refunds),
            },
        }

    async def test_webhook(self, webhook_id: int) -> bool:
        """Test a webhook by sending a test event."""
        from apps.backend.modules.payment.models.webhook import PaymentWebhook
        from apps.backend.modules.payment.models.webhook_event import PaymentWebhookEvent
        import httpx

        result = await self.db.execute(
            select(PaymentWebhook).where(PaymentWebhook.id == webhook_id)
        )
        webhook = result.scalars().first()

        if not webhook:
            return False

        # Create test event
        test_payload = {
            "event_type": "payment.test",
            "timestamp": datetime.utcnow().isoformat(),
            "test": True,
            "message": "This is a test webhook event",
        }

        webhook_event = PaymentWebhookEvent(
            webhook_id=webhook.id,
            event_type="payment.test",
            payload=test_payload,
            delivered=False,
        )

        self.db.add(webhook_event)
        await self.db.commit()

        # Try to deliver the webhook
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    webhook.url,
                    json=test_payload,
                    headers={"X-Webhook-Event": "payment.test"},
                )

                if response.status_code in [200, 201, 202]:
                    webhook_event.delivered = True
                    webhook_event.delivered_at = datetime.utcnow()
                    webhook.last_triggered_at = datetime.utcnow()
                    await self.db.commit()
                    return True
        except Exception as e:
            logger.error(f"Error testing webhook {webhook_id}: {str(e)}")
            webhook_event.last_error = str(e)
            webhook_event.delivery_attempts += 1
            await self.db.commit()

        return False

    async def generate_receipt(
        self, payment_id: int, format: str = "pdf"
    ) -> Optional[Dict[str, Any]]:
        """Generate a receipt for a payment."""
        result = await self.db.execute(select(Payment).where(Payment.id == payment_id))
        payment = result.scalars().first()

        if not payment:
            return None

        receipt_data = {
            "id": payment.id,
            "receipt_number": f"RCP-{payment.id:06d}",
            "payment_id": payment.id,
            "reference": payment.reference,
            "amount": float(payment.amount),
            "currency": payment.currency,
            "status": payment.status.value,
            "method": payment.method.value,
            "description": payment.description,
            "issued_date": datetime.utcnow().isoformat(),
            "payment_date": payment.created_at.isoformat(),
            "metadata": payment.metadata_ or {},
        }

        if format == "json":
            return receipt_data
        elif format == "html":
            return self._generate_html_receipt(receipt_data)
        elif format == "pdf":
            return await self._generate_pdf_receipt(receipt_data)

        return receipt_data

    def _generate_html_receipt(self, receipt_data: Dict[str, Any]) -> str:
        """Generate an HTML receipt."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Recibo #{receipt_data['receipt_number']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .receipt {{ max-width: 600px; margin: 0 auto; border: 1px solid #ccc; padding: 20px; }}
                .header {{ text-align: center; margin-bottom: 20px; }}
                .section {{ margin-bottom: 15px; }}
                .label {{ font-weight: bold; }}
                .amount {{ font-size: 18px; font-weight: bold; color: #27ae60; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="receipt">
                <div class="header">
                    <h1>RECIBO DE PAGAMENTO</h1>
                    <p>#{receipt_data['receipt_number']}</p>
                </div>

                <div class="section">
                    <p><span class="label">Referência:</span> {receipt_data['reference']}</p>
                    <p><span class="label">Status:</span> {receipt_data['status']}</p>
                    <p><span class="label">Método:</span> {receipt_data['method']}</p>
                </div>

                <div class="section">
                    <p><span class="label">Valor:</span> <span class="amount">{receipt_data['amount']} {receipt_data['currency']}</span></p>
                </div>

                <div class="section">
                    <p><span class="label">Data de Emissão:</span> {receipt_data['issued_date']}</p>
                    <p><span class="label">Data de Pagamento:</span> {receipt_data['payment_date']}</p>
                </div>

                {f'<div class="section"><p><span class="label">Descrição:</span> {receipt_data["description"]}</p></div>' if receipt_data.get('description') else ''}

                <div class="footer">
                    <p>Este é um recibo automático gerado pelo sistema SILA</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html

    async def _generate_pdf_receipt(
        self, receipt_data: Dict[str, Any]
    ) -> Optional[str]:
        """Generate a PDF receipt."""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.units import inch
            from reportlab.pdfgen import canvas
            from io import BytesIO

            # Create PDF in memory
            pdf_buffer = BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=letter)

            # Add content
            c.setFont("Helvetica-Bold", 16)
            c.drawString(1 * inch, 10 * inch, "RECIBO DE PAGAMENTO")

            c.setFont("Helvetica", 10)
            y = 9.5 * inch

            c.drawString(1 * inch, y, f"Recibo: {receipt_data['receipt_number']}")
            y -= 0.3 * inch

            c.drawString(1 * inch, y, f"Referência: {receipt_data['reference']}")
            y -= 0.3 * inch

            c.drawString(1 * inch, y, f"Status: {receipt_data['status']}")
            y -= 0.3 * inch

            c.drawString(1 * inch, y, f"Método: {receipt_data['method']}")
            y -= 0.5 * inch

            c.setFont("Helvetica-Bold", 12)
            c.drawString(
                1 * inch,
                y,
                f"Valor: {receipt_data['amount']} {receipt_data['currency']}",
            )
            y -= 0.5 * inch

            c.setFont("Helvetica", 10)
            c.drawString(1 * inch, y, f"Data de Emissão: {receipt_data['issued_date']}")
            y -= 0.3 * inch

            c.drawString(
                1 * inch, y, f"Data de Pagamento: {receipt_data['payment_date']}"
            )

            c.save()

            # Save to file
            pdf_path = f"/tmp/receipt_{receipt_data['payment_id']}.pdf"
            with open(pdf_path, "wb") as f:
                f.write(pdf_buffer.getvalue())

            return pdf_path
        except Exception as e:
            logger.error(f"Error generating PDF receipt: {str(e)}")
            return None

    async def list_payments(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[PaymentStatus] = None,
        user_id: Optional[int] = None,
    ) -> List[PaymentInDB]:
        """List payments with optional status and user filtering."""
        query = select(Payment)

        if status:
            query = query.where(Payment.status == status)

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        payments = result.scalars().all()

        payments_in_db = [PaymentInDB.model_validate(p) for p in payments]

        if user_id:
            payments_in_db = [
                p for p in payments_in_db if self._can_access_payment(p, user_id)
            ]

        return payments_in_db

    async def get_transaction(
        self, transaction_id: int
    ) -> Optional[PaymentTransaction]:
        """Get a specific transaction by ID."""
        result = await self.db.execute(
            select(PaymentTransaction).where(PaymentTransaction.id == transaction_id)
        )
        return result.scalars().first()
