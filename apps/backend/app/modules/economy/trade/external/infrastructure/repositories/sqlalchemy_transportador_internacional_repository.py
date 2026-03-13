from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.economy.trade.external.application.ports import TransportadorInternacionalRepositoryPort
from app.modules.economy.trade.external.domain.models import TransportadorInternacional
from app.modules.economy.trade.external.infrastructure.models import TransportadorInternacionalModel
from app.modules.economy.trade.external.infrastructure.repositories.sqlalchemy_operador_logistico_repository_base import SQLAlchemyOperadorLogisticoRepositoryBase

class SQLAlchemyTransportadorInternacionalRepository(SQLAlchemyOperadorLogisticoRepositoryBase[TransportadorInternacional, TransportadorInternacionalModel], TransportadorInternacionalRepositoryPort):

    def __init__(self, session: AsyncSession):
        super().__init__(session, model_cls=TransportadorInternacionalModel, domain_cls=TransportadorInternacional)