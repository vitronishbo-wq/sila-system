"""Public safety bridge exports for economy integrations."""
from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.public_security.application.ports.ocorrencia_repository_port import OcorrenciaRepositoryPort
from apps.backend.app.modules.public_security.domain.enums import PrioridadeOcorrencia, StatusOcorrencia, TipoOcorrencia
from apps.backend.app.modules.public_security.infrastructure.models.ocorrencia_model import OcorrenciaModel
from apps.backend.app.modules.public_security.infrastructure.repositories.sqlalchemy_ocorrencia_repository import SQLAlchemyOcorrenciaRepository

def make_ocorrencia_repository(db: AsyncSession) -> SQLAlchemyOcorrenciaRepository:
    return SQLAlchemyOcorrenciaRepository(db)
__all__ = ['OcorrenciaModel', 'OcorrenciaRepositoryPort', 'PrioridadeOcorrencia', 'SQLAlchemyOcorrenciaRepository', 'StatusOcorrencia', 'TipoOcorrencia', 'make_ocorrencia_repository']