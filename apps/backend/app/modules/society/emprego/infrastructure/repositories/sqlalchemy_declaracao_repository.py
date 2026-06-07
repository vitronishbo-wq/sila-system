from apps.backend.app.modules.society.emprego.application.ports import DeclaracaoRepositoryPort
from apps.backend.app.modules.society.emprego.infrastructure.models.declaracao_model import (
    DeclaracaoModel,
)
from apps.backend.app.modules.society.emprego.infrastructure.repositories._workflow_sqlalchemy_repository import (
    SQLAlchemyWorkflowRepository,
)


class SQLAlchemyDeclaracaoRepository(SQLAlchemyWorkflowRepository, DeclaracaoRepositoryPort):
    def __init__(self, session):
        super().__init__(session, DeclaracaoModel)
