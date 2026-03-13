from apps.backend.app.modules.society.emprego.application.ports import FiscalizacaoRepositoryPort
from apps.backend.app.modules.society.emprego.infrastructure.models.fiscalizacao_model import FiscalizacaoModel
from apps.backend.app.modules.society.emprego.infrastructure.repositories._workflow_sqlalchemy_repository import SQLAlchemyWorkflowRepository

class SQLAlchemyFiscalizacaoRepository(SQLAlchemyWorkflowRepository, FiscalizacaoRepositoryPort):

    def __init__(self, session):
        super().__init__(session, FiscalizacaoModel)