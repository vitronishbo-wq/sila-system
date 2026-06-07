from apps.backend.app.modules.society.desporto.infrastructure.repositories.sqlalchemy_atleta_repository import (
    SQLAlchemyAtletaRepository,
)
from apps.backend.app.modules.society.desporto.infrastructure.repositories.sqlalchemy_clube_repository import (
    SQLAlchemyClubeRepository,
)
from apps.backend.app.modules.society.desporto.infrastructure.repositories.sqlalchemy_competicao_repository import (
    SQLAlchemyCompeticaoRepository,
)
from apps.backend.app.modules.society.desporto.infrastructure.repositories.sqlalchemy_estadio_repository import (
    SQLAlchemyEstadioRepository,
)
from apps.backend.app.modules.society.desporto.infrastructure.repositories.sqlalchemy_jogo_repository import (
    SQLAlchemyJogoRepository,
)

__all__ = [
    "SQLAlchemyAtletaRepository",
    "SQLAlchemyCompeticaoRepository",
    "SQLAlchemyClubeRepository",
    "SQLAlchemyJogoRepository",
    "SQLAlchemyEstadioRepository",
]
