"""Repository for transaction CRUD operations."""

from typing import Any, Dict, List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from modules.payment.models.transaction import PaymentTransaction
from modules.payment.models.enums import TransactionStatus, TransactionType
from modules.payment.schemas.payment import TransactionResponse


class TransactionRepository:
    """Repository for transaction database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, transaction_data: Dict[str, Any]) -> TransactionResponse:
        """Create a new transaction."""
        # Convert metadata_ to metadata if present
        if "metadata_" in transaction_data:
            transaction_data["metadata"] = transaction_data.pop("metadata_")

        transaction = PaymentTransaction(**transaction_data)
        self.db.add(transaction)
        await self.db.commit()
        await self.db.refresh(transaction)
        return TransactionResponse.model_validate(transaction)

    async def get_by_id(self, transaction_id: int) -> Optional[TransactionResponse]:
        """Get transaction by ID."""
        result = await self.db.execute(
            select(PaymentTransaction).where(PaymentTransaction.id == transaction_id)
        )
        transaction = result.scalars().first()
        return TransactionResponse.model_validate(transaction) if transaction else None

    async def get_by_reference(self, reference: str) -> Optional[TransactionResponse]:
        """Get transaction by reference."""
        result = await self.db.execute(
            select(PaymentTransaction).where(PaymentTransaction.reference == reference)
        )
        transaction = result.scalars().first()
        return TransactionResponse.model_validate(transaction) if transaction else None

    async def get_by_payment_id(
        self, payment_id: int, skip: int = 0, limit: int = 100
    ) -> List[TransactionResponse]:
        """Get transactions by payment ID."""
        result = await self.db.execute(
            select(PaymentTransaction)
            .where(PaymentTransaction.payment_id == payment_id)
            .offset(skip)
            .limit(limit)
            .order_by(PaymentTransaction.created_at.desc())
        )
        transactions = result.scalars().all()
        return [TransactionResponse.model_validate(t) for t in transactions]

    async def get_multi(
        self, skip: int = 0, limit: int = 100
    ) -> List[TransactionResponse]:
        """Get multiple transactions."""
        result = await self.db.execute(
            select(PaymentTransaction)
            .offset(skip)
            .limit(limit)
            .order_by(PaymentTransaction.created_at.desc())
        )
        transactions = result.scalars().all()
        return [TransactionResponse.model_validate(t) for t in transactions]

    async def update_status(
        self, transaction_id: int, status: TransactionStatus
    ) -> Optional[TransactionResponse]:
        """Update transaction status."""
        result = await self.db.execute(
            select(PaymentTransaction).where(PaymentTransaction.id == transaction_id)
        )
        transaction = result.scalars().first()
        if not transaction:
            return None

        transaction.status = status
        await self.db.commit()
        await self.db.refresh(transaction)
        return TransactionResponse.model_validate(transaction)

    async def update_provider_reference(
        self, transaction_id: int, provider_reference: str
    ) -> Optional[TransactionResponse]:
        """Update transaction provider reference."""
        result = await self.db.execute(
            select(PaymentTransaction).where(PaymentTransaction.id == transaction_id)
        )
        transaction = result.scalars().first()
        if not transaction:
            return None

        transaction.provider_reference = provider_reference
        await self.db.commit()
        await self.db.refresh(transaction)
        return TransactionResponse.model_validate(transaction)

    async def get_latest_by_payment_id(
        self, payment_id: int
    ) -> Optional[TransactionResponse]:
        """Get the latest transaction for a payment."""
        result = await self.db.execute(
            select(PaymentTransaction)
            .where(PaymentTransaction.payment_id == payment_id)
            .order_by(PaymentTransaction.created_at.desc())
            .limit(1)
        )
        transaction = result.scalars().first()
        return TransactionResponse.model_validate(transaction) if transaction else None

    async def get_statistics(self) -> Dict[str, Any]:
        """Get transaction statistics."""
        total_transactions = await self.db.scalar(
            select(func.count(PaymentTransaction.id))
        )
        total_amount = await self.db.scalar(select(func.sum(PaymentTransaction.amount)))

        completed_transactions = await self.db.scalar(
            select(func.count(PaymentTransaction.id)).where(
                PaymentTransaction.status == TransactionStatus.COMPLETED
            )
        )
        completed_amount = await self.db.scalar(
            select(func.sum(PaymentTransaction.amount)).where(
                PaymentTransaction.status == TransactionStatus.COMPLETED
            )
        )

        payment_transactions = await self.db.scalar(
            select(func.count(PaymentTransaction.id)).where(
                PaymentTransaction.type == TransactionType.PAYMENT
            )
        )
        refund_transactions = await self.db.scalar(
            select(func.count(PaymentTransaction.id)).where(
                PaymentTransaction.type == TransactionType.REFUND
            )
        )

        return {
            "total_transactions": total_transactions or 0,
            "total_amount": float(total_amount or 0),
            "completed_transactions": completed_transactions or 0,
            "completed_amount": float(completed_amount or 0),
            "payment_transactions": payment_transactions or 0,
            "refund_transactions": refund_transactions or 0,
        }
