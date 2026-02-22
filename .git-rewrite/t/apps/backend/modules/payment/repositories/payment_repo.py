"""Repository for payment CRUD operations."""

from typing import Any, Dict, List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from modules.payment.models.payment import Payment
from modules.payment.models.enums import PaymentStatus, PaymentMethod
from modules.payment.schemas.payment import (
    PaymentCreate,
    PaymentUpdate,
    PaymentInDB,
    PaymentFilter,
)


class PaymentRepository:
    """Repository for payment database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, payment_data: PaymentCreate) -> PaymentInDB:
        """Create a new payment."""
        payment = Payment(**payment_data.model_dump())
        self.db.add(payment)
        await self.db.commit()
        await self.db.refresh(payment)
        return PaymentInDB.model_validate(payment)

    async def get_by_id(self, payment_id: int) -> Optional[PaymentInDB]:
        """Get payment by ID."""
        result = await self.db.execute(select(Payment).where(Payment.id == payment_id))
        payment = result.scalars().first()
        return PaymentInDB.model_validate(payment) if payment else None

    async def get_by_reference(self, reference: str) -> Optional[PaymentInDB]:
        """Get payment by reference."""
        result = await self.db.execute(
            select(Payment).where(Payment.reference == reference)
        )
        payment = result.scalars().first()
        return PaymentInDB.model_validate(payment) if payment else None

    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[PaymentInDB]:
        """Get multiple payments."""
        result = await self.db.execute(
            select(Payment)
            .offset(skip)
            .limit(limit)
            .order_by(Payment.created_at.desc())
        )
        payments = result.scalars().all()
        return [PaymentInDB.model_validate(p) for p in payments]

    async def get_filtered(
        self, filters: PaymentFilter, skip: int = 0, limit: int = 100
    ) -> List[PaymentInDB]:
        """Get payments with filters."""
        query = select(Payment)

        if filters.status:
            query = query.where(Payment.status == filters.status)
        if filters.method:
            query = query.where(Payment.method == filters.method)
        if filters.date_from:
            query = query.where(Payment.created_at >= filters.date_from)
        if filters.date_to:
            query = query.where(Payment.created_at <= filters.date_to)
        if filters.min_amount is not None:
            query = query.where(Payment.amount >= filters.min_amount)
        if filters.max_amount is not None:
            query = query.where(Payment.amount <= filters.max_amount)

        result = await self.db.execute(
            query.offset(skip).limit(limit).order_by(Payment.created_at.desc())
        )
        payments = result.scalars().all()
        return [PaymentInDB.model_validate(p) for p in payments]

    async def update(
        self, payment: Payment, update_data: PaymentUpdate
    ) -> Optional[PaymentInDB]:
        """Update a payment."""
        if not payment:
            return None

        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(payment, field, value)

        await self.db.commit()
        await self.db.refresh(payment)
        return PaymentInDB.model_validate(payment)

    async def delete(self, payment_id: int) -> bool:
        """Delete a payment."""
        result = await self.db.execute(select(Payment).where(Payment.id == payment_id))
        payment = result.scalars().first()
        if payment:
            await self.db.delete(payment)
            await self.db.commit()
            return True
        return False

    async def get_statistics(self) -> Dict[str, Any]:
        """Get payment statistics."""
        total_payments = await self.db.scalar(select(func.count(Payment.id)))
        total_amount = await self.db.scalar(select(func.sum(Payment.amount)))

        completed_payments = await self.db.scalar(
            select(func.count(Payment.id)).where(
                Payment.status == PaymentStatus.COMPLETED
            )
        )
        completed_amount = await self.db.scalar(
            select(func.sum(Payment.amount)).where(
                Payment.status == PaymentStatus.COMPLETED
            )
        )

        return {
            "total_payments": total_payments or 0,
            "total_amount": float(total_amount or 0),
            "completed_payments": completed_payments or 0,
            "completed_amount": float(completed_amount or 0),
            "pending_payments": (total_payments or 0) - (completed_payments or 0),
        }
