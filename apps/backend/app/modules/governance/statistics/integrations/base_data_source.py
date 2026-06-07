from __future__ import annotations

from collections.abc import Iterable
from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDataSource:
    """Base utilitaria para consultas agregadas de metricas."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def _scalar(self, statement, default=0):
        result = await self.db.execute(statement)
        value = result.scalar()
        return default if value is None else value

    @staticmethod
    def _month_window(data_ref: date) -> tuple[date, date]:
        start = data_ref.replace(day=1)
        next_month = (start + timedelta(days=32)).replace(day=1)
        return (start, next_month)

    @staticmethod
    def _status_in_ci(column, statuses: Iterable[str]):
        return func.lower(column).in_([value.lower() for value in statuses])

    @staticmethod
    def _as_float(value: Decimal | float | int | None) -> float:
        if value is None:
            return 0.0
        if isinstance(value, Decimal):
            return float(value)
        return float(value)
