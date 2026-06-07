"""Student Number Generator — ENS-YYYY-XXXXXXXX format.

Format: ENS-{year}-{sequential 8-digit}
Example: ENS-2026-00001234

Sequential counter persisted in a DB table so it survives restarts.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.educacao.infrastructure.models.student_number_counter import (
    StudentNumberCounter,
)


def _pad(n: int) -> str:
    return str(n).zfill(8)


class StudentNumberGenerator:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def generate(self) -> str:
        year = str(datetime.utcnow().year)
        stmt = pg_insert(StudentNumberCounter).values(
            year=year, last_sequence=1
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=["year"],
            set_={"last_sequence": StudentNumberCounter.last_sequence + 1},
        )
        stmt = stmt.returning(StudentNumberCounter.last_sequence)
        result = await self.session.execute(stmt)
        seq = result.scalar_one()
        return f"ENS-{year}-{_pad(seq)}"
