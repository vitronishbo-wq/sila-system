from apps.backend.app.modules.society.emprego.application.ports import InscricaoRepositoryPort
from apps.backend.app.modules.society.emprego.infrastructure.models.inscricao_model import (
    InscricaoModel,
)
from apps.backend.app.modules.society.emprego.infrastructure.repositories._workflow_sqlalchemy_repository import (
    SQLAlchemyWorkflowRepository,
)


class SQLAlchemyInscricaoRepository(SQLAlchemyWorkflowRepository, InscricaoRepositoryPort):
    def __init__(self, session):
        super().__init__(session, InscricaoModel)
