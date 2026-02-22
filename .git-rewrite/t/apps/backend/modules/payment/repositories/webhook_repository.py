"""Webhook repository for payment webhooks."""

from typing import List, Optional
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.webhook import PaymentWebhook
from ..models.webhook_event import PaymentWebhookEvent


class WebhookRepository:
    """Repository for webhook operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_webhook(
        self,
        url: str,
        events: List[str],
        secret_key: Optional[str] = None,
    ) -> PaymentWebhook:
        """Create a new webhook."""
        webhook = PaymentWebhook(
            url=url,
            events=events,
            secret_key=secret_key,
            active=True,
        )
        self.db.add(webhook)
        await self.db.commit()
        await self.db.refresh(webhook)
        return webhook

    async def get_webhook(self, webhook_id: int) -> Optional[PaymentWebhook]:
        """Get a webhook by ID."""
        result = await self.db.execute(
            select(PaymentWebhook).where(PaymentWebhook.id == webhook_id)
        )
        return result.scalar_one_or_none()

    async def get_webhooks(
        self,
        active_only: bool = True,
        skip: int = 0,
        limit: int = 100,
    ) -> List[PaymentWebhook]:
        """Get webhooks with optional filtering."""
        query = select(PaymentWebhook)

        if active_only:
            query = query.where(PaymentWebhook.active == True)

        result = await self.db.execute(
            query.offset(skip).limit(limit).order_by(PaymentWebhook.created_at.desc())
        )
        return result.scalars().all()

    async def get_webhooks_for_event(self, event_type: str) -> List[PaymentWebhook]:
        """Get all webhooks that should receive an event."""
        result = await self.db.execute(
            select(PaymentWebhook).where(PaymentWebhook.active == True)
        )
        webhooks = result.scalars().all()

        # Filter webhooks that have this event in their events list
        return [w for w in webhooks if event_type in w.events]

    async def update_webhook(
        self,
        webhook_id: int,
        url: Optional[str] = None,
        events: Optional[List[str]] = None,
        active: Optional[bool] = None,
    ) -> Optional[PaymentWebhook]:
        """Update a webhook."""
        webhook = await self.get_webhook(webhook_id)
        if not webhook:
            return None

        if url:
            webhook.url = url
        if events:
            webhook.events = events
        if active is not None:
            webhook.active = active

        webhook.updated_at = datetime.utcnow()
        self.db.add(webhook)
        await self.db.commit()
        await self.db.refresh(webhook)
        return webhook

    async def delete_webhook(self, webhook_id: int) -> bool:
        """Delete a webhook."""
        webhook = await self.get_webhook(webhook_id)
        if not webhook:
            return False

        await self.db.delete(webhook)
        await self.db.commit()
        return True

    async def log_webhook_event(
        self,
        webhook_id: int,
        event_type: str,
        payload: dict,
        payment_id: Optional[int] = None,
    ) -> PaymentWebhookEvent:
        """Log a webhook event."""
        event = PaymentWebhookEvent(
            webhook_id=webhook_id,
            payment_id=payment_id,
            event_type=event_type,
            payload=payload,
            delivered=False,
        )
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event

    async def get_webhook_events(
        self,
        webhook_id: Optional[int] = None,
        delivered: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[PaymentWebhookEvent]:
        """Get webhook events with optional filtering."""
        query = select(PaymentWebhookEvent)

        if webhook_id:
            query = query.where(PaymentWebhookEvent.webhook_id == webhook_id)
        if delivered is not None:
            query = query.where(PaymentWebhookEvent.delivered == delivered)

        result = await self.db.execute(
            query.offset(skip)
            .limit(limit)
            .order_by(PaymentWebhookEvent.created_at.desc())
        )
        return result.scalars().all()

    async def mark_event_delivered(
        self,
        event_id: int,
    ) -> Optional[PaymentWebhookEvent]:
        """Mark a webhook event as delivered."""
        result = await self.db.execute(
            select(PaymentWebhookEvent).where(PaymentWebhookEvent.id == event_id)
        )
        event = result.scalar_one_or_none()

        if not event:
            return None

        event.delivered = True
        event.delivered_at = datetime.utcnow()
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event

    async def increment_delivery_attempts(
        self,
        event_id: int,
        error_message: Optional[str] = None,
    ) -> Optional[PaymentWebhookEvent]:
        """Increment delivery attempts for a webhook event."""
        result = await self.db.execute(
            select(PaymentWebhookEvent).where(PaymentWebhookEvent.id == event_id)
        )
        event = result.scalar_one_or_none()

        if not event:
            return None

        event.delivery_attempts += 1
        if error_message:
            event.last_error = error_message

        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event

    async def get_pending_events(self, limit: int = 100) -> List[PaymentWebhookEvent]:
        """Get pending webhook events to deliver."""
        result = await self.db.execute(
            select(PaymentWebhookEvent)
            .where(PaymentWebhookEvent.delivered == False)
            .where(PaymentWebhookEvent.delivery_attempts < 5)
            .order_by(PaymentWebhookEvent.created_at.asc())
            .limit(limit)
        )
        return result.scalars().all()
