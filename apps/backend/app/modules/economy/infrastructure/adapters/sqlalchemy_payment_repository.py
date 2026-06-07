from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.models.enums import PaymentStatus
from ...domain.models.payment import Payment
from ...domain.ports.payment_repository_port import PaymentRepositoryPort
from ..models import EconomyPaymentModel


class SQLAlchemyPaymentRepository(PaymentRepositoryPort):
    """Adapter: SQLAlchemy implementation of PaymentRepositoryPort for Economy module."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, payment: Payment) -> Payment:
        """Create a new payment."""
        model = self._to_model(payment)
        self.session.add(model)
        await self.session.flush()
        return self._to_domain(model)

    async def save(self, payment: Payment) -> Payment:
        """Save/update a payment."""
        model = self._to_model(payment)
        await self.session.merge(model)
        await self.session.flush()
        return self._to_domain(model)

    async def get_by_id(self, payment_id: str) -> Payment | None:
        """Get payment by ID."""
        result = await self.session.execute(
            select(EconomyPaymentModel).where(EconomyPaymentModel.id == payment_id)
        )
        model = result.scalars().first()
        return self._to_domain(model) if model else None

    async def get_by_citizen(self, citizen_id: str) -> list[Payment]:
        """Get all payments for citizen."""
        result = await self.session.execute(
            select(EconomyPaymentModel)
            .where(EconomyPaymentModel.citizen_id == citizen_id)
            .order_by(EconomyPaymentModel.created_at.desc())
        )
        return [self._to_domain(item) for item in result.scalars().all()]

    async def list_by_invoice(self, invoice_id: str) -> list[Payment]:
        """List payments for invoice."""
        result = await self.session.execute(
            select(EconomyPaymentModel)
            .where(EconomyPaymentModel.invoice_id == invoice_id)
            .order_by(EconomyPaymentModel.created_at.desc())
        )
        return [self._to_domain(item) for item in result.scalars().all()]

    async def get_by_gateway_ref(self, gateway_reference: str) -> Payment | None:
        """Get payment by gateway reference."""
        result = await self.session.execute(
            select(EconomyPaymentModel).where(
                EconomyPaymentModel.gateway_reference == gateway_reference
            )
        )
        model = result.scalars().first()
        return self._to_domain(model) if model else None

    async def exists_by_gateway_ref(self, gateway_reference: str) -> bool:
        """Check if gateway reference exists."""
        result = await self.session.execute(
            select(EconomyPaymentModel.id).where(
                EconomyPaymentModel.gateway_reference == gateway_reference
            )
        )
        return result.first() is not None

    async def list_all(self, limit: int = 100, offset: int = 0) -> list[Payment]:
        """List all payments."""
        result = await self.session.execute(
            select(EconomyPaymentModel)
            .order_by(EconomyPaymentModel.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return [self._to_domain(item) for item in result.scalars().all()]

    async def delete(self, payment_id: str) -> bool:
        """Delete a payment."""
        result = await self.session.execute(
            delete(EconomyPaymentModel).where(EconomyPaymentModel.id == payment_id)
        )
        await self.session.flush()
        return result.rowcount > 0

    @staticmethod
    def _to_model(payment: Payment) -> EconomyPaymentModel:
        return EconomyPaymentModel(
            id=payment.id,
            invoice_id=payment.invoice_id,
            citizen_id=payment.citizen_id,
            amount=payment.amount,
            currency=payment.currency,
            gateway_reference=payment.gateway_reference,
            payment_method=payment.payment_method,
            status=payment.status.value
            if hasattr(payment.status, "value")
            else str(payment.status),
            created_at=payment.created_at,
            confirmed_at=payment.confirmed_at,
        )

    @staticmethod
    def _to_domain(model: EconomyPaymentModel) -> Payment:
        try:
            status = PaymentStatus(model.status)
        except Exception:
            status = PaymentStatus.PENDING
        return Payment(
            id=model.id,
            invoice_id=model.invoice_id,
            citizen_id=model.citizen_id,
            amount=float(model.amount),
            currency=model.currency,
            gateway_reference=model.gateway_reference,
            payment_method=model.payment_method,
            status=status,
            created_at=model.created_at,
            confirmed_at=model.confirmed_at,
        )
