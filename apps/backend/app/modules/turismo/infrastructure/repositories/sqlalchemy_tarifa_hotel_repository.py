from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.turismo.application.ports.tarifa_hotel_repository_port import TarifaHotelRepositoryPort


class SQLAlchemyTarifaHotelRepository(TarifaHotelRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session
