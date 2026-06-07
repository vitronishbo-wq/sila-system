from apps.backend.app.modules.educacao.application.ports import BoletimRepositoryPort
from apps.backend.app.modules.educacao.infrastructure.models.boletim_model import BoletimModel
from apps.backend.app.modules.educacao.infrastructure.repositories._workflow_sqlalchemy_repository import (
    SQLAlchemyWorkflowRepository,
)


class SQLAlchemyBoletimRepository(SQLAlchemyWorkflowRepository, BoletimRepositoryPort):
    def __init__(self, session):
        super().__init__(session, BoletimModel)
