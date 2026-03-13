from app.modules.society.emprego.application.ports import ResultadoRepositoryPort
from app.modules.society.emprego.infrastructure.models.resultado_model import ResultadoModel
from app.modules.society.emprego.infrastructure.repositories._workflow_sqlalchemy_repository import SQLAlchemyWorkflowRepository

class SQLAlchemyResultadoRepository(SQLAlchemyWorkflowRepository, ResultadoRepositoryPort):

    def __init__(self, session):
        super().__init__(session, ResultadoModel)