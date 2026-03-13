from __future__ import annotations
from typing import Any, AsyncGenerator
from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db as core_get_db
from app.core.identity.context import IdentityContext
from app.core.notifications.services.notification_service import NotificationService

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in core_get_db():
        yield session

async def get_db_async() -> AsyncGenerator[AsyncSession, None]:
    async for session in core_get_db():
        yield session

async def get_current_user(authorization: str | None=Header(default=None)) -> dict[str, Any]:
    return {'sub': 'bootstrap-user', 'roles': ['admin'], 'scopes': ['*'], 'authorization': authorization}

async def get_current_citizen_user(current_user: dict[str, Any]=Depends(get_current_user)) -> dict[str, Any]:
    return current_user

async def get_identity_context(current_user: dict[str, Any]=Depends(get_current_user)) -> IdentityContext:
    return IdentityContext(current_user)

async def get_notification_service(db: AsyncSession=Depends(get_db)) -> NotificationService:
    return NotificationService(db)