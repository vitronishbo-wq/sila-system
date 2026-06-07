from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.repositories.sqlalchemy_desapropriacao_repository import (
    SQLAlchemyDesapropriacaoRepository,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.repositories.sqlalchemy_georreferenciamento_repository import (
    SQLAlchemyGeorreferenciamentoRepository,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.repositories.sqlalchemy_imovel_repository import (
    SQLAlchemyImovelRepository,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.repositories.sqlalchemy_matricula_imovel_repository import (
    SQLAlchemyMatriculaImovelRepository,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.repositories.sqlalchemy_oneracao_repository import (
    SQLAlchemyOneracaoRepository,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.repositories.sqlalchemy_proprietario_repository import (
    SQLAlchemyProprietarioRepository,
)

__all__ = [
    "SQLAlchemyImovelRepository",
    "SQLAlchemyProprietarioRepository",
    "SQLAlchemyOneracaoRepository",
    "SQLAlchemyDesapropriacaoRepository",
    "SQLAlchemyMatriculaImovelRepository",
    "SQLAlchemyGeorreferenciamentoRepository",
]
