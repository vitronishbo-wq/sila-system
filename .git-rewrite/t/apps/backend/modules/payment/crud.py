"""CRUD operations for payment module with standardized data access."""

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.payment.models.payment import Payment
from modules.payment.schemas.payment import (
    PaymentCreate,
    PaymentFilter,
    PaymentInDB,
    PaymentUpdate,
)
from modules.payment.models.enums import PaymentStatus


class PaymentCRUD:
    """CRUD operations for payments."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, obj_in: PaymentCreate, created_by: int) -> PaymentInDB:
        """Create a new payment."""
        if not obj_in.reference:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            obj_in.reference = f"PAY-{timestamp}-{created_by}"

        db_obj = Payment(**obj_in.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return PaymentInDB.model_validate(db_obj)

    async def get(self, payment_id: int) -> Optional[PaymentInDB]:
        """Get a payment by ID."""
        result = await self.db.execute(select(Payment).where(Payment.id == payment_id))
        db_obj = result.scalar_one_or_none()
        return PaymentInDB.model_validate(db_obj) if db_obj else None

    async def get_by_reference(self, reference: str) -> Optional[PaymentInDB]:
        """Get a payment by reference."""
        result = await self.db.execute(
            select(Payment).where(Payment.reference == reference)
        )
        db_obj = result.scalar_one_or_none()
        return PaymentInDB.model_validate(db_obj) if db_obj else None

    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[PaymentInDB]:
        """Get multiple payments."""
        result = await self.db.execute(
            select(Payment)
            .offset(skip)
            .limit(limit)
            .order_by(Payment.created_at.desc())
        )
        db_objs = result.scalars().all()
        return [PaymentInDB.model_validate(obj) for obj in db_objs]

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
        db_objs = result.scalars().all()
        return [PaymentInDB.model_validate(obj) for obj in db_objs]

    async def update(self, db_obj: Payment, obj_in: PaymentUpdate) -> PaymentInDB:
        """Update a payment."""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return PaymentInDB.model_validate(db_obj)

    async def delete(self, payment_id: int) -> bool:
        """Delete a payment."""
        result = await self.db.execute(select(Payment).where(Payment.id == payment_id))
        db_obj = result.scalar_one_or_none()
        if db_obj:
            await self.db.delete(db_obj)
            await self.db.commit()
            return True
        return False

    async def get_statistics(self) -> Dict[str, Any]:
        """Get payment statistics."""
        base_query = select(Payment)

        total_payments = await self.db.scalar(
            select(func.count()).select_from(base_query.subquery())
        )
        total_amount = await self.db.scalar(
            select(func.sum(Payment.amount)).select_from(base_query.subquery())
        )
        completed_payments = await self.db.scalar(
            select(func.count()).select_from(
                base_query.where(Payment.status == PaymentStatus.COMPLETED).subquery()
            )
        )
        completed_amount = await self.db.scalar(
            select(func.sum(Payment.amount)).select_from(
                base_query.where(Payment.status == PaymentStatus.COMPLETED).subquery()
            )
        )

        return {
            "total_payments": total_payments or 0,
            "total_amount": float(total_amount or Decimal("0")),
            "completed_payments": completed_payments or 0,
            "completed_amount": float(completed_amount or Decimal("0")),
            "pending_payments": (total_payments or 0) - (completed_payments or 0),
        }


def get_payment_crud(db: AsyncSession) -> PaymentCRUD:
    """Factory function for dependency injection."""
    return PaymentCRUD(db)
