from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.models.payment import Payment
from apps.backend.app.modules.payment.domain.ports.payment_repository_port import (
    PaymentRepositoryPort,
)
from apps.backend.app.modules.payment.infrastructure.orm.payment_model import PaymentModel


class SQLAlchemyPaymentRepository(PaymentRepositoryPort):
    """Adapter: SQLAlchemy implementation of PaymentRepositoryPort."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, payment: Payment) -> Payment:
        """Create and persist a new payment."""
        model = PaymentModel.from_domain(payment)
        self.session.add(model)
        await self.session.flush()
        return model.to_domain()

    async def save(self, payment: Payment) -> Payment:
        """Update an existing payment."""
        model = PaymentModel.from_domain(payment)
        await self.session.merge(model)
        await self.session.flush()
        return payment

    async def get_by_id(self, payment_id: str) -> Payment | None:
        """Retrieve payment by ID."""
        stmt = select(PaymentModel).where(PaymentModel.id == payment_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_domain() if model else None

    async def get_by_reference(self, reference: str) -> Payment | None:
        """Retrieve payment by reference."""
        stmt = select(PaymentModel).where(PaymentModel.reference == reference)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_domain() if model else None

    async def list_by_citizen(
        self, citizen_id: str, limit: int = 100, offset: int = 0
    ) -> list[Payment]:
        """List payments for a citizen."""
        stmt = (
            select(PaymentModel)
            .where(PaymentModel.citizen_id == citizen_id)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [m.to_domain() for m in models]

    async def list_by_status(self, status: str, limit: int = 100, offset: int = 0) -> list[Payment]:
        """List payments by status."""
        stmt = select(PaymentModel).where(PaymentModel.status == status).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [m.to_domain() for m in models]

    async def list_all(self, limit: int = 100, offset: int = 0) -> list[Payment]:
        """List all payments."""
        stmt = select(PaymentModel).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [m.to_domain() for m in models]

    async def delete(self, payment_id: str) -> bool:
        """Delete a payment."""
        stmt = select(PaymentModel).where(PaymentModel.id == payment_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.flush()
            return True
        return False

    async def exists(self, payment_id: str) -> bool:
        """Check if payment exists."""
        stmt = select(PaymentModel).where(PaymentModel.id == payment_id).limit(1)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
