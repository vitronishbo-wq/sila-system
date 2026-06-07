from __future__ import annotations

from datetime import date
from uuid import UUID, uuid4

from apps.backend.app.core.bridges import CitizenRepositoryPort, ServiceRequestLifecycleBridge
from apps.backend.app.modules.educacao.application.ports.workflow_repository_port import (
    WorkflowRepositoryPort,
)
from apps.backend.app.modules.educacao.domain.models._workflow_record import WorkflowRecord
from apps.backend.app.modules.educacao.exceptions import CitizenNotFoundError


class WorkflowService:
    def __init__(
        self,
        repository: WorkflowRepositoryPort,
        process_prefix: str,
        citizen_repo: CitizenRepositoryPort | None = None,
        request_service: ServiceRequestLifecycleBridge | None = None,
    ):
        self.repository = repository
        self.process_prefix = process_prefix
        self.citizen_repo = citizen_repo
        self.request_service = request_service

    async def create_record(
        self,
        *,
        service_type: str,
        citizen_id: UUID,
        instituicao_id: UUID,
        observacoes: str | None = None,
        metadata: dict | None = None,
    ) -> WorkflowRecord:
        if self.citizen_repo is not None:
            citizen = await self.citizen_repo.get_by_id(citizen_id)
            if not citizen:
                raise CitizenNotFoundError(f"Cidadao {citizen_id} nao encontrado")
        exists = await self.repository.exists_active_for_citizen(citizen_id, service_type)
        if exists:
            raise ValueError("Cidadao ja possui registo ativo para este servico")
        year = date.today().year
        numero = await self.repository.next_numero_processo(year, service_type, self.process_prefix)
        record = WorkflowRecord(
            id=uuid4(),
            numero_processo=numero,
            service_type=service_type,
            citizen_id=citizen_id,
            instituicao_id=instituicao_id,
            data_registo=date.today(),
            observacoes=observacoes,
            metadata=metadata or {},
        )
        saved = await self.repository.save(record)
        if self.request_service is not None:
            await self.request_service.create_education_request(
                entity_id=saved.id,
                citizen_id=saved.citizen_id,
                numero_processo=saved.numero_processo,
                escola_nome=service_type.replace("_", " "),
                ano_letivo=str(year),
            )
        return saved

    async def conclude_record(
        self, record_id: UUID, actor_id: UUID, resumo: str | None = None
    ) -> WorkflowRecord:
        record = await self.repository.get_by_id(record_id)
        if not record:
            raise ValueError("Registo nao encontrado")
        record.concluir(resumo)
        updated = await self.repository.save(record)
        if self.request_service is not None:
            await self.request_service.mark_education_request_completed(
                entity_id=updated.id,
                actor_id=actor_id,
                metadata={"status": "concluida", "service_type": updated.service_type},
            )
        return updated

    async def cancel_record(self, record_id: UUID, actor_id: UUID, motivo: str) -> WorkflowRecord:
        record = await self.repository.get_by_id(record_id)
        if not record:
            raise ValueError("Registo nao encontrado")
        record.cancelar(motivo)
        updated = await self.repository.save(record)
        if self.request_service is not None:
            await self.request_service.mark_education_request_completed(
                entity_id=updated.id,
                actor_id=actor_id,
                metadata={
                    "status": "cancelada",
                    "service_type": updated.service_type,
                    "motivo": motivo,
                },
            )
        return updated

    async def get_record(self, record_id: UUID) -> WorkflowRecord | None:
        return await self.repository.get_by_id(record_id)

    async def list_records(
        self, citizen_id: UUID, service_type: str | None = None
    ) -> list[WorkflowRecord]:
        return await self.repository.list_by_citizen(citizen_id, service_type)
