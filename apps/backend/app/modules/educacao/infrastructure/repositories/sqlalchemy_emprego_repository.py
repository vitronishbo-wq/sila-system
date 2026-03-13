from apps.backend.app.modules.educacao.application.ports import EmpregoRepositoryPort
from apps.backend.app.modules.educacao.infrastructure.models.emprego_model import EmpregoModel
from apps.backend.app.modules.educacao.infrastructure.repositories._workflow_sqlalchemy_repository import SQLAlchemyWorkflowRepository

class SQLAlchemyEmpregoRepository(SQLAlchemyWorkflowRepository, EmpregoRepositoryPort):

    def __init__(self, session):
        super().__init__(session, EmpregoModel)