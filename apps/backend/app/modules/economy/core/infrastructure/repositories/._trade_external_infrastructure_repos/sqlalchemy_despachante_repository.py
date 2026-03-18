from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.economy.trade.external.application.ports import DespachanteRepositoryPort
from apps.backend.app.modules.economy.trade.external.domain.models import Despachante
from apps.backend.app.modules.economy.trade.external.infrastructure.models import DespachanteModel
from apps.backend.app.modules.economy.trade.external.infrastructure.repositories.sqlalchemy_operador_logistico_repository_base import SQLAlchemyOperadorLogisticoRepositoryBase

class SQLAlchemyDespachanteRepository(SQLAlchemyOperadorLogisticoRepositoryBase[Despachante, DespachanteModel], DespachanteRepositoryPort):

    def __init__(self, session: AsyncSession):
        super().__init__(session, model_cls=DespachanteModel, domain_cls=Despachante)