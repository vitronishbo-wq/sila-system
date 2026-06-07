from apps.backend.app.modules.educacao.application.ports import UniversidadeRepositoryPort
from apps.backend.app.modules.educacao.infrastructure.models.universidade_model import (
    UniversidadeModel,
)
from apps.backend.app.modules.educacao.infrastructure.repositories._workflow_sqlalchemy_repository import (
    SQLAlchemyWorkflowRepository,
)


class SQLAlchemyUniversidadeRepository(SQLAlchemyWorkflowRepository, UniversidadeRepositoryPort):
    def __init__(self, session):
        super().__init__(session, UniversidadeModel)
