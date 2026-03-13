from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import and_, func, select
from app.modules.society.emprego.application.ports.workflow_repository_port import WorkflowRepositoryPort
from app.modules.society.emprego.domain.enums import WorkflowStatus
from app.modules.society.emprego.domain.models._workflow_record import WorkflowEmpregoRecord

class SQLAlchemyWorkflowRepository(WorkflowRepositoryPort):

    def __init__(self, session, model_cls):
        self.session = session
        self.model_cls = model_cls

    async def save(self, item: WorkflowEmpregoRecord) -> WorkflowEmpregoRecord:
        model = await self.session.get(self.model_cls, item.id)
        if not model:
            model = self.model_cls(id=item.id)
            self.session.add(model)
        model.numero_processo = item.numero_processo
        model.citizen_id = item.citizen_id
        model.data_registro = item.data_registro
        model.service_type = item.service_type
        model.status = item.status.value
        model.observacoes = item.observacoes
        model.metadata_json = item.metadata or {}
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, item_id: UUID):
        model = await self.session.get(self.model_cls, item_id)
        return self._to_domain(model) if model else None

    async def list_by_citizen(self, citizen_id: UUID, service_type: str | None=None):
        stmt = select(self.model_cls).where(self.model_cls.citizen_id == citizen_id)
        if service_type:
            stmt = stmt.where(self.model_cls.service_type == service_type)
        rows = (await self.session.execute(stmt.order_by(self.model_cls.data_registro.desc()))).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def exists_active_for_citizen(self, citizen_id: UUID, service_type: str) -> bool:
        stmt = select(self.model_cls.id).where(and_(self.model_cls.citizen_id == citizen_id, self.model_cls.service_type == service_type, self.model_cls.status.in_([WorkflowStatus.PENDENTE.value, WorkflowStatus.EM_ANALISE.value, WorkflowStatus.APROVADA.value])))
        return (await self.session.execute(stmt)).first() is not None

    async def next_numero_processo(self, ano: int, prefix: str) -> str:
        pattern = f'{prefix}/{ano}/%'
        stmt = select(func.count()).select_from(self.model_cls).where(self.model_cls.numero_processo.like(pattern))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'{prefix}/{ano}/{count + 1:04d}'

    @staticmethod
    def _to_domain(model) -> WorkflowEmpregoRecord:
        return WorkflowEmpregoRecord(id=model.id, numero_processo=model.numero_processo, citizen_id=model.citizen_id, data_registro=model.data_registro or date.today(), service_type=model.service_type, status=WorkflowStatus(model.status), observacoes=model.observacoes, metadata=model.metadata_json or {})