from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from app.modules.educacao.application.ports import TransferenciaRepositoryPort
from app.modules.educacao.domain.enums import StatusFluxo
from app.modules.educacao.domain.models._workflow_record import WorkflowRecord
from app.modules.educacao.infrastructure.models.transferencia_model import TransferenciaModel
from app.modules.educacao.infrastructure.repositories._workflow_sqlalchemy_repository import SQLAlchemyWorkflowRepository

class SQLAlchemyTransferenciaRepository(SQLAlchemyWorkflowRepository, TransferenciaRepositoryPort):

    def __init__(self, session):
        super().__init__(session, TransferenciaModel)

    async def get_active_by_matricula(self, matricula_id: UUID) -> WorkflowRecord | None:
        stmt = select(TransferenciaModel).where(TransferenciaModel.service_type == 'transferencia', TransferenciaModel.metadata_json['matricula_origem_id'].astext == str(matricula_id), TransferenciaModel.status.in_([StatusFluxo.PENDENTE.value, StatusFluxo.CONFIRMADA.value, StatusFluxo.EM_ANALISE.value])).order_by(TransferenciaModel.data_registo.desc()).limit(1)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None