from apps.backend.app.modules.society.emprego.application.ports import CertificacaoRepositoryPort
from apps.backend.app.modules.society.emprego.infrastructure.models.certificacao_model import CertificacaoModel
from apps.backend.app.modules.society.emprego.infrastructure.repositories._workflow_sqlalchemy_repository import SQLAlchemyWorkflowRepository

class SQLAlchemyCertificacaoRepository(SQLAlchemyWorkflowRepository, CertificacaoRepositoryPort):

    def __init__(self, session):
        super().__init__(session, CertificacaoModel)