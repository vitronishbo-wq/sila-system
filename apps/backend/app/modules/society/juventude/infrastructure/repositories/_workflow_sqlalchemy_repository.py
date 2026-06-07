from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import and_, func, select

from apps.backend.app.modules.society.juventude.application.ports.workflow_repository_port import (
    WorkflowRepositoryPort,
)
from apps.backend.app.modules.society.juventude.domain.enums import StatusFluxo
from apps.backend.app.modules.society.juventude.domain.models._workflow_record import WorkflowRecord


class SQLAlchemyWorkflowRepository(WorkflowRepositoryPort):
    def __init__(self, session, model_cls):
        self.session = session
        self.model_cls = model_cls

    async def save(self, item: WorkflowRecord) -> WorkflowRecord:
        model = await self.session.get(self.model_cls, item.id)
        if not model:
            model = self.model_cls(id=item.id)
            self.session.add(model)
        model.numero_processo = item.numero_processo
        model.service_type = item.service_type
        model.citizen_id = item.citizen_id
        model.instituicao_id = item.instituicao_id
        model.data_registo = item.data_registo
        model.status = item.status.value
        model.observacoes = item.observacoes
        model.metadata_json = item.metadata or {}
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, item_id: UUID) -> WorkflowRecord | None:
        model = await self.session.get(self.model_cls, item_id)
        return self._to_domain(model) if model else None

    async def list_by_citizen(
        self, citizen_id: UUID, service_type: str | None = None
    ) -> list[WorkflowRecord]:
        stmt = select(self.model_cls).where(self.model_cls.citizen_id == citizen_id)
        if service_type:
            stmt = stmt.where(self.model_cls.service_type == service_type)
        stmt = stmt.order_by(self.model_cls.data_registo.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def exists_active_for_citizen(self, citizen_id: UUID, service_type: str) -> bool:
        stmt = select(self.model_cls.id).where(
            and_(
                self.model_cls.citizen_id == citizen_id,
                self.model_cls.service_type == service_type,
                self.model_cls.status.in_(
                    [
                        StatusFluxo.PENDENTE.value,
                        StatusFluxo.CONFIRMADA.value,
                        StatusFluxo.EM_ANALISE.value,
                        StatusFluxo.APROVADA.value,
                    ]
                ),
            )
        )
        return (await self.session.execute(stmt)).first() is not None

    async def next_numero_processo(self, ano: int, service_type: str, process_prefix: str) -> str:
        prefix = f"{process_prefix}/{service_type.upper()}/{ano}/"
        stmt = (
            select(func.count())
            .select_from(self.model_cls)
            .where(self.model_cls.numero_processo.like(f"{prefix}%"))
        )
        count = (await self.session.execute(stmt)).scalar() or 0
        return f"{prefix}{count + 1:04d}"

    @staticmethod
    def _to_domain(model) -> WorkflowRecord:
        return WorkflowRecord(
            id=model.id,
            numero_processo=model.numero_processo,
            service_type=model.service_type,
            citizen_id=model.citizen_id,
            instituicao_id=model.instituicao_id,
            data_registo=model.data_registo or date.today(),
            status=StatusFluxo(model.status),
            observacoes=model.observacoes,
            metadata=model.metadata_json or {},
        )
