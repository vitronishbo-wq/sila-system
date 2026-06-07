from apps.backend.app.modules.society.emprego.application.ports import ConcursoRepositoryPort
from apps.backend.app.modules.society.emprego.infrastructure.models.concurso_model import (
    ConcursoModel,
)
from apps.backend.app.modules.society.emprego.infrastructure.repositories._workflow_sqlalchemy_repository import (
    SQLAlchemyWorkflowRepository,
)


class SQLAlchemyConcursoRepository(SQLAlchemyWorkflowRepository, ConcursoRepositoryPort):
    def __init__(self, session):
        super().__init__(session, ConcursoModel)
