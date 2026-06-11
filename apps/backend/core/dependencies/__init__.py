"""Centralized dependency injection - Single source for all dependencies."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.core.db import AsyncSessionLocal


# Database
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session dependency.

    Usage:
        @app.get("/users")
        async def list_users(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        yield session


# Event Bus
def get_events():
    """Get event bus dependency.

    Usage:
        @app.post("/payments")
        async def create_payment(
            data: PaymentCreate,
            events = Depends(get_events)
        ):
            from apps.backend.app.core.events import get_event_bus
            bus = get_event_bus()
            await bus.publish("payment.created", {...})
    """
    from apps.backend.app.core.events import get_event_bus

    return get_event_bus()


# IAM
def get_iam_client():
    """Get IAM client dependency.

    Usage:
        @app.get("/protected")
        async def protected(iam = Depends(get_iam_client)):
            user = iam.get_current_user(token)
    """
    from apps.backend.core.security import IAMClient
    return IAMClient()
