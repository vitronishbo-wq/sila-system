from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.tourism.application.ports.licenca_turismo_repository_port import LicencaTurismoRepositoryPort

class SQLAlchemyLicencaTurismoRepository(LicencaTurismoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session