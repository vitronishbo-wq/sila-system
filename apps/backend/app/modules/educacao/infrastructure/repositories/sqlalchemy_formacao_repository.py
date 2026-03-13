from apps.backend.app.modules.educacao.application.ports import FormacaoRepositoryPort
from apps.backend.app.modules.educacao.infrastructure.models.formacao_model import FormacaoModel
from apps.backend.app.modules.educacao.infrastructure.repositories._workflow_sqlalchemy_repository import SQLAlchemyWorkflowRepository

class SQLAlchemyFormacaoRepository(SQLAlchemyWorkflowRepository, FormacaoRepositoryPort):

    def __init__(self, session):
        super().__init__(session, FormacaoModel)