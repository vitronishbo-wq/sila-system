from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.educacao.infrastructure.models.idempotency_model import (
    IdempotencyModel,
)

IDEMPOTENCY_TTL_HOURS = 24


class IdempotencyService:
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def make_key(operation: str, *parts: str) -> str:
        raw = f"{operation}:{':'.join(str(p) for p in parts)}"
        return hashlib.sha256(raw.encode()).hexdigest()

    async def is_duplicate(self, idempotency_key: str) -> bool:
        stmt = select(IdempotencyModel).where(
            IdempotencyModel.id == idempotency_key,
            IdempotencyModel.expires_at > datetime.now(timezone.utc),
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def try_lock(self, idempotency_key: str, operation: str) -> bool:
        stmt = (
            pg_insert(IdempotencyModel)
            .values(
                id=idempotency_key,
                operation=operation,
                expires_at=datetime.now(timezone.utc) + timedelta(hours=IDEMPOTENCY_TTL_HOURS),
            )
            .on_conflict_do_nothing()
        )
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def complete(self, idempotency_key: str, result: Any = None) -> None:
        stmt = select(IdempotencyModel).where(IdempotencyModel.id == idempotency_key)
        model = (await self.session.execute(stmt)).scalar_one_or_none()
        if model:
            model.result = result

    async def execute_once(
        self, operation: str, key_parts: list[str], fn, **fn_kwargs
    ) -> dict[str, Any]:
        idem_key = self.make_key(operation, *key_parts)
        if await self.is_duplicate(idem_key):
            return {"duplicated": True, "idempotency_key": idem_key}
        locked = await self.try_lock(idem_key, operation)
        if not locked:
            return {"duplicated": True, "idempotency_key": idem_key}
        result = await fn(**fn_kwargs)
        await self.complete(idem_key, result)
        return {"duplicated": False, "idempotency_key": idem_key, "result": result}
