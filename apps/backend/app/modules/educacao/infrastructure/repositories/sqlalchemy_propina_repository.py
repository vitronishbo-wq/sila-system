from app.modules.educacao.application.ports import PropinaRepositoryPort
from app.modules.educacao.infrastructure.models.propina_model import PropinaModel
from app.modules.educacao.infrastructure.repositories._workflow_sqlalchemy_repository import SQLAlchemyWorkflowRepository


class SQLAlchemyPropinaRepository(SQLAlchemyWorkflowRepository, PropinaRepositoryPort):
    def __init__(self, session):
        super().__init__(session, PropinaModel)
