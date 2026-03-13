from app.modules.society.emprego.application.ports import AlfabetizacaoRepositoryPort
from app.modules.society.emprego.infrastructure.models.alfabetizacao_model import AlfabetizacaoModel
from app.modules.society.emprego.infrastructure.repositories._workflow_sqlalchemy_repository import SQLAlchemyWorkflowRepository

class SQLAlchemyAlfabetizacaoRepository(SQLAlchemyWorkflowRepository, AlfabetizacaoRepositoryPort):

    def __init__(self, session):
        super().__init__(session, AlfabetizacaoModel)