from app.modules.educacao.application.ports import TransferenciaRepositoryPort
from app.modules.educacao.infrastructure.models.transferencia_model import TransferenciaModel
from app.modules.educacao.infrastructure.repositories._workflow_sqlalchemy_repository import SQLAlchemyWorkflowRepository


class SQLAlchemyTransferenciaRepository(SQLAlchemyWorkflowRepository, TransferenciaRepositoryPort):
    def __init__(self, session):
        super().__init__(session, TransferenciaModel)
