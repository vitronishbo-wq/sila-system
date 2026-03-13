from app.modules.society.emprego.application.ports import MediacaoRepositoryPort
from app.modules.society.emprego.infrastructure.models.mediacao_model import MediacaoModel
from app.modules.society.emprego.infrastructure.repositories._workflow_sqlalchemy_repository import SQLAlchemyWorkflowRepository

class SQLAlchemyMediacaoRepository(SQLAlchemyWorkflowRepository, MediacaoRepositoryPort):

    def __init__(self, session):
        super().__init__(session, MediacaoModel)