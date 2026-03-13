from apps.backend.app.modules.society.emprego.application.ports import AvaliacaoRepositoryPort
from apps.backend.app.modules.society.emprego.infrastructure.models.avaliacao_model import AvaliacaoModel
from apps.backend.app.modules.society.emprego.infrastructure.repositories._workflow_sqlalchemy_repository import SQLAlchemyWorkflowRepository

class SQLAlchemyAvaliacaoRepository(SQLAlchemyWorkflowRepository, AvaliacaoRepositoryPort):

    def __init__(self, session):
        super().__init__(session, AvaliacaoModel)