from apps.backend.app.modules.society.emprego.application.ports import FormacaoRepositoryPort
from apps.backend.app.modules.society.emprego.infrastructure.models.formacao_avancada_model import FormacaoAvancadaModel
from apps.backend.app.modules.society.emprego.infrastructure.repositories._workflow_sqlalchemy_repository import SQLAlchemyWorkflowRepository

class SQLAlchemyFormacaoAvancadaRepository(SQLAlchemyWorkflowRepository, FormacaoRepositoryPort):

    def __init__(self, session):
        super().__init__(session, FormacaoAvancadaModel)