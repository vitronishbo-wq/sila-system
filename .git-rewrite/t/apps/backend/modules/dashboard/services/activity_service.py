"""
Stub ActivityService for dashboard module.
Provides minimal methods expected by the dashboard package so the app
can start. Expand with real logic as needed.
"""

from typing import Any, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession


class ActivityService:
    """Simple placeholder for activity related operations."""

    def __init__(self, db: Optional[AsyncSession] = None):
        self.db = db

    async def list_recent_activities(self, limit: int = 10) -> Dict[str, Any]:
        return {"total": 0, "activities": []}

    async def record_activity(
        self,
        action: str,
        user_id: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        # no-op placeholder
        return None
