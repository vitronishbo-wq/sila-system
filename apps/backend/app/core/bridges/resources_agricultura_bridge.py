"""Agriculture bridge exports for economy integrations."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.resources.agricultura.application.ports.produtor_repository_port import (
    ProdutorRepositoryPort,
)
from apps.backend.app.modules.resources.agricultura.domain.enums import StatusProdutor, TipoProdutor
from apps.backend.app.modules.resources.agricultura.infrastructure.models.produtor_model import (
    ProdutorModel,
)
from apps.backend.app.modules.resources.agricultura.infrastructure.repositories.sqlalchemy_produtor_repository import (
    SQLAlchemyProdutorRepository,
)


def make_agricultura_produtor_repository(db: AsyncSession) -> SQLAlchemyProdutorRepository:
    return SQLAlchemyProdutorRepository(db)


__all__ = [
    "ProdutorModel",
    "ProdutorRepositoryPort",
    "SQLAlchemyProdutorRepository",
    "StatusProdutor",
    "TipoProdutor",
    "make_agricultura_produtor_repository",
]
