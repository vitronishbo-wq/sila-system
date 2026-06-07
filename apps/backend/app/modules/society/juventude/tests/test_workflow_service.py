from __future__ import annotations

import asyncio
from datetime import date
from uuid import UUID, uuid4

import pytest

from apps.backend.app.modules.society.juventude.application.ports.workflow_repository_port import (
    WorkflowRepositoryPort,
)
from apps.backend.app.modules.society.juventude.application.services.workflow_service import (
    WorkflowService,
)
from apps.backend.app.modules.society.juventude.domain.enums import StatusFluxo
from apps.backend.app.modules.society.juventude.domain.models._workflow_record import WorkflowRecord
from apps.backend.app.modules.society.juventude.tests._fakes import FakeCitizenService


class InMemoryWorkflowRepository(WorkflowRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, WorkflowRecord] = {}

    async def save(self, item: WorkflowRecord) -> WorkflowRecord:
        self._items[item.id] = item
        return item

    async def get_by_id(self, item_id: UUID) -> WorkflowRecord | None:
        return self._items.get(item_id)

    async def list_by_citizen(
        self, citizen_id: UUID, service_type: str | None = None
    ) -> list[WorkflowRecord]:
        values = [i for i in self._items.values() if i.citizen_id == citizen_id]
        if service_type:
            values = [i for i in values if i.service_type == service_type]
        return sorted(values, key=lambda i: i.data_registo, reverse=True)

    async def exists_active_for_citizen(self, citizen_id: UUID, service_type: str) -> bool:
        active = {
            StatusFluxo.PENDENTE,
            StatusFluxo.CONFIRMADA,
            StatusFluxo.EM_ANALISE,
            StatusFluxo.APROVADA,
        }
        return any(
            i.citizen_id == citizen_id and i.service_type == service_type and (i.status in active)
            for i in self._items.values()
        )

    async def next_numero_processo(self, ano: int, service_type: str, process_prefix: str) -> str:
        prefix = f"{process_prefix}/{service_type.upper()}/{ano}/"
        count = sum(1 for i in self._items.values() if i.numero_processo.startswith(prefix))
        return f"{prefix}{count + 1:04d}"


def test_workflow_create_e_concluir() -> None:

    async def scenario() -> None:
        citizen_id = uuid4()
        service = WorkflowService(
            repository=InMemoryWorkflowRepository(),
            process_prefix="JUV",
            citizen_service=FakeCitizenService(active=True),
        )
        created = await service.create_record(
            service_type="inscricao_programa",
            citizen_id=citizen_id,
            instituicao_id=uuid4(),
            observacoes="solicitacao inicial",
        )
        updated = await service.conclude_record(created.id, "concluida")
        assert created.numero_processo.startswith(f"JUV/INSCRICAO_PROGRAMA/{date.today().year}/")
        assert updated.status == StatusFluxo.CONCLUIDA

    asyncio.run(scenario())


def test_workflow_bloqueia_duplicado_ativo() -> None:

    async def scenario() -> None:
        citizen_id = uuid4()
        service = WorkflowService(
            repository=InMemoryWorkflowRepository(),
            process_prefix="JUV",
            citizen_service=FakeCitizenService(active=True),
        )
        await service.create_record(
            service_type="inscricao_programa", citizen_id=citizen_id, instituicao_id=uuid4()
        )
        with pytest.raises(ValueError, match="ativo"):
            await service.create_record(
                service_type="inscricao_programa", citizen_id=citizen_id, instituicao_id=uuid4()
            )

    asyncio.run(scenario())
