from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.tourism.application.ports.reserva_pacote_repository_port import ReservaPacoteRepositoryPort

class SQLAlchemyReservaPacoteRepository(ReservaPacoteRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session
