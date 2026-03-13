from app.modules.society.emprego.application.ports import OfertaRepositoryPort
from app.modules.society.emprego.infrastructure.models.oferta_model import OfertaModel
from app.modules.society.emprego.infrastructure.repositories._workflow_sqlalchemy_repository import SQLAlchemyWorkflowRepository

class SQLAlchemyOfertaRepository(SQLAlchemyWorkflowRepository, OfertaRepositoryPort):

    def __init__(self, session):
        super().__init__(session, OfertaModel)