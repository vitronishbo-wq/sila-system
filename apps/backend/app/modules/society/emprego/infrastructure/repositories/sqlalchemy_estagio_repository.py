from apps.backend.app.modules.society.emprego.application.ports import EstagioRepositoryPort
from apps.backend.app.modules.society.emprego.infrastructure.models.estagio_model import EstagioModel
from apps.backend.app.modules.society.emprego.infrastructure.repositories._workflow_sqlalchemy_repository import SQLAlchemyWorkflowRepository

class SQLAlchemyEstagioRepository(SQLAlchemyWorkflowRepository, EstagioRepositoryPort):

    def __init__(self, session):
        super().__init__(session, EstagioModel)