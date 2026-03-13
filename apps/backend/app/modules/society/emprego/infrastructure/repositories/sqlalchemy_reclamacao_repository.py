from app.modules.society.emprego.application.ports import ReclamacaoRepositoryPort
from app.modules.society.emprego.infrastructure.models.reclamacao_model import ReclamacaoModel
from app.modules.society.emprego.infrastructure.repositories._workflow_sqlalchemy_repository import SQLAlchemyWorkflowRepository

class SQLAlchemyReclamacaoRepository(SQLAlchemyWorkflowRepository, ReclamacaoRepositoryPort):

    def __init__(self, session):
        super().__init__(session, ReclamacaoModel)