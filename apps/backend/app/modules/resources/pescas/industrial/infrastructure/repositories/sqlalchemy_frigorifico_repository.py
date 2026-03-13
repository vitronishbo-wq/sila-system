from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession

class SqlalchemyFrigorificoRepository:

    def __init__(self, session: AsyncSession | None=None):
        self.session = session