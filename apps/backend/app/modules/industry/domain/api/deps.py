from apps.backend.app.modules.industry.application.services.estabelecimento_industrial_service import (
    EstabelecimentoIndustrialService,
)
from apps.backend.app.modules.industry.infrastructure.repositories.sqlalchemy_estabelecimento_industrial_repository import (
    SQLAlchemyEstabelecimentoIndustrialRepository,
)


def get_estabelecimento_industrial_service() -> EstabelecimentoIndustrialService:
    repository = SQLAlchemyEstabelecimentoIndustrialRepository()
    return EstabelecimentoIndustrialService(repository=repository)
