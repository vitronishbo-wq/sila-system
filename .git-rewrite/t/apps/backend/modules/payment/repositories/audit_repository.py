"""Audit repository for payment operations."""

from typing import List, Optional, Dict, Any
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.audit_log import PaymentAuditLog


class AuditRepository:
    """Repository for audit log operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_action(
        self,
        action: str,
        payment_id: Optional[int] = None,
        user_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None,
    ) -> PaymentAuditLog:
        """Log an action to the audit log."""
        log = PaymentAuditLog(
            payment_id=payment_id,
            action=action,
            user_id=user_id,
            ip_address=ip_address,
            details=details or {},
            error_message=error_message,
        )
        self.db.add(log)
        await self.db.commit()
        await self.db.refresh(log)
        return log

    async def get_logs(
        self,
        payment_id: Optional[int] = None,
        action: Optional[str] = None,
        user_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[PaymentAuditLog]:
        """Get audit logs with optional filters."""
        query = select(PaymentAuditLog)

        if payment_id:
            query = query.where(PaymentAuditLog.payment_id == payment_id)
        if action:
            query = query.where(PaymentAuditLog.action == action)
        if user_id:
            query = query.where(PaymentAuditLog.user_id == user_id)

        result = await self.db.execute(
            query.offset(skip).limit(limit).order_by(PaymentAuditLog.created_at.desc())
        )
        return result.scalars().all()

    async def get_payment_history(self, payment_id: int) -> List[PaymentAuditLog]:
        """Get complete history of a payment."""
        result = await self.db.execute(
            select(PaymentAuditLog)
            .where(PaymentAuditLog.payment_id == payment_id)
            .order_by(PaymentAuditLog.created_at.asc())
        )
        return result.scalars().all()

    async def get_user_actions(
        self, user_id: int, limit: int = 100
    ) -> List[PaymentAuditLog]:
        """Get all actions performed by a user."""
        result = await self.db.execute(
            select(PaymentAuditLog)
            .where(PaymentAuditLog.user_id == user_id)
            .order_by(PaymentAuditLog.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()

    async def get_failed_actions(self, limit: int = 100) -> List[PaymentAuditLog]:
        """Get all failed actions."""
        result = await self.db.execute(
            select(PaymentAuditLog)
            .where(PaymentAuditLog.error_message.isnot(None))
            .order_by(PaymentAuditLog.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()

    async def get_action_count(
        self,
        action: str,
        payment_id: Optional[int] = None,
        days: Optional[int] = None,
    ) -> int:
        """Get count of actions."""
        query = select(PaymentAuditLog).where(PaymentAuditLog.action == action)

        if payment_id:
            query = query.where(PaymentAuditLog.payment_id == payment_id)

        if days:
            from datetime import timedelta

            cutoff_date = datetime.utcnow() - timedelta(days=days)
            query = query.where(PaymentAuditLog.created_at >= cutoff_date)

        result = await self.db.execute(query)
        return len(result.scalars().all())

    async def delete_old_logs(self, days: int = 90) -> int:
        """Delete audit logs older than specified days."""
        from datetime import timedelta
        from sqlalchemy import delete

        cutoff_date = datetime.utcnow() - timedelta(days=days)
        stmt = delete(PaymentAuditLog).where(PaymentAuditLog.created_at < cutoff_date)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.rowcount
