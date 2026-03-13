from app.modules.society.emprego.application.ports import ContratoRepositoryPort
from app.modules.society.emprego.infrastructure.models.contrato_model import ContratoModel
from app.modules.society.emprego.infrastructure.repositories._workflow_sqlalchemy_repository import SQLAlchemyWorkflowRepository

class SQLAlchemyContratoRepository(SQLAlchemyWorkflowRepository, ContratoRepositoryPort):

    def __init__(self, session):
        super().__init__(session, ContratoModel)