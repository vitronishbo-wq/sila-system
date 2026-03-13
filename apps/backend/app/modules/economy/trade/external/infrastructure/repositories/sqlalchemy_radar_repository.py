from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.economy.trade.external.application.ports import RadarRepositoryPort
from app.modules.economy.trade.external.domain.models import Radar
from app.modules.economy.trade.external.infrastructure.models import RadarModel
from app.modules.economy.trade.external.infrastructure.repositories.sqlalchemy_operador_logistico_repository_base import SQLAlchemyOperadorLogisticoRepositoryBase

class SQLAlchemyRadarRepository(SQLAlchemyOperadorLogisticoRepositoryBase[Radar, RadarModel], RadarRepositoryPort):

    def __init__(self, session: AsyncSession):
        super().__init__(session, model_cls=RadarModel, domain_cls=Radar)