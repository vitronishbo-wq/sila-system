"""Core dependencies - centralized"""

from apps.backend.app.core.db import get_db
from apps.backend.app.core.events import get_event_bus
from core.security import IAMClient
from fastapi.security import HTTPBearer

security = HTTPBearer(auto_error=False)


async def get_iam() -> IAMClient:
    """IAM client dependency"""
    return IAMClient()


async def get_events():
    """Event bus dependency"""
    return get_event_bus()


__all__ = ["get_db", "get_iam", "get_events", "security"]
