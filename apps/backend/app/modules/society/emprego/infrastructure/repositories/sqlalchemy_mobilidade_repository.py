from apps.backend.app.modules.society.emprego.application.ports import MobilidadeRepositoryPort
from apps.backend.app.modules.society.emprego.infrastructure.models.mobilidade_model import (
    MobilidadeModel,
)
from apps.backend.app.modules.society.emprego.infrastructure.repositories._workflow_sqlalchemy_repository import (
    SQLAlchemyWorkflowRepository,
)


class SQLAlchemyMobilidadeRepository(SQLAlchemyWorkflowRepository, MobilidadeRepositoryPort):
    def __init__(self, session):
        super().__init__(session, MobilidadeModel)
