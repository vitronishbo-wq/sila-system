from apps.backend.app.modules.educacao.application.ports import CertificadoRepositoryPort
from apps.backend.app.modules.educacao.infrastructure.models.certificado_model import CertificadoModel
from apps.backend.app.modules.educacao.infrastructure.repositories._workflow_sqlalchemy_repository import SQLAlchemyWorkflowRepository

class SQLAlchemyCertificadoRepository(SQLAlchemyWorkflowRepository, CertificadoRepositoryPort):

    def __init__(self, session):
        super().__init__(session, CertificadoModel)