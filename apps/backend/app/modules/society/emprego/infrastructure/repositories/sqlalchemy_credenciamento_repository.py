from app.modules.society.emprego.application.ports import CredenciamentoRepositoryPort
from app.modules.society.emprego.infrastructure.models.credenciamento_model import CredenciamentoModel
from app.modules.society.emprego.infrastructure.repositories._workflow_sqlalchemy_repository import SQLAlchemyWorkflowRepository

class SQLAlchemyCredenciamentoRepository(SQLAlchemyWorkflowRepository, CredenciamentoRepositoryPort):

    def __init__(self, session):
        super().__init__(session, CredenciamentoModel)