from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.tourism.application.ports.reserva_hotel_repository_port import ReservaHotelRepositoryPort

class SQLAlchemyReservaHotelRepository(ReservaHotelRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session