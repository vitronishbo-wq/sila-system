from apps.backend.app.modules.civil_protection.infrastructure.repositories.sqlalchemy_atendimento_repository import (
    SQLAlchemyAtendimentoRepository,
)
from apps.backend.app.modules.civil_protection.infrastructure.repositories.sqlalchemy_bombeiro_repository import (
    SQLAlchemyBombeiroRepository,
)
from apps.backend.app.modules.civil_protection.infrastructure.repositories.sqlalchemy_corporacao_repository import (
    SQLAlchemyCorporacaoRepository,
)
from apps.backend.app.modules.civil_protection.infrastructure.repositories.sqlalchemy_despacho_repository import (
    SQLAlchemyDespachoRepository,
)
from apps.backend.app.modules.civil_protection.infrastructure.repositories.sqlalchemy_ocorrencia_emergencial_repository import (
    SQLAlchemyOcorrenciaEmergencialRepository,
)

__all__ = [
    "SQLAlchemyCorporacaoRepository",
    "SQLAlchemyBombeiroRepository",
    "SQLAlchemyOcorrenciaEmergencialRepository",
    "SQLAlchemyDespachoRepository",
    "SQLAlchemyAtendimentoRepository",
]
