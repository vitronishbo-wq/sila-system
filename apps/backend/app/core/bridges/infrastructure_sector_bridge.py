"""Infrastructure sector bridge exports for optional economy integrations."""

from apps.backend.app.modules.infrastructure_sector.logistica.transport.infrastructure.repositories.sqlalchemy_viagem_repository import (
    SQLAlchemyViagemRepository,
)
from apps.backend.app.modules.infrastructure_sector.obras_publicas.infrastructure.repositories.sqlalchemy_obra_repository import (
    SQLAlchemyObraRepository,
)
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.infrastructure.repositories.sqlalchemy_alvara_repository import (
    SQLAlchemyAlvaraRepository,
)

__all__ = ["SQLAlchemyAlvaraRepository", "SQLAlchemyObraRepository", "SQLAlchemyViagemRepository"]
