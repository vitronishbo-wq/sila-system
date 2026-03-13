from __future__ import annotations
from datetime import date
from uuid import UUID, uuid4
from app.modules.society.juventude.application.ports.citizen_service_port import CitizenServicePort
from app.modules.society.juventude.application.ports.request_service_port import RequestServicePort
from app.modules.society.juventude.application.ports.workflow_repository_port import WorkflowRepositoryPort
from app.modules.society.juventude.domain.models._workflow_record import WorkflowRecord

class WorkflowService:

    def __init__(self, *, repository: WorkflowRepositoryPort, process_prefix: str, citizen_service: CitizenServicePort | None=None, request_service: RequestServicePort | None=None) -> None:
        self.repository = repository
        self.process_prefix = process_prefix
        self.citizen_service = citizen_service
        self.request_service = request_service

    async def create_record(self, *, service_type: str, citizen_id: UUID, instituicao_id: UUID, observacoes: str | None=None, metadata: dict | None=None) -> WorkflowRecord:
        if self.citizen_service is not None:
            if not await self.citizen_service.is_citizen_active(citizen_id):
                raise ValueError('Cidadao nao encontrado ou inativo')
        if await self.repository.exists_active_for_citizen(citizen_id, service_type):
            raise ValueError('Cidadao ja possui registo ativo para este servico')
        year = date.today().year
        numero = await self.repository.next_numero_processo(year, service_type, self.process_prefix)
        record = WorkflowRecord(id=uuid4(), numero_processo=numero, service_type=service_type, citizen_id=citizen_id, instituicao_id=instituicao_id, data_registo=date.today(), observacoes=observacoes, metadata=metadata or {})
        saved = await self.repository.save(record)
        if self.request_service is not None:
            await self.request_service.create_request(request_type=f'WORKFLOW_{service_type.upper()}', entity_id=saved.id, citizen_id=saved.citizen_id, numero_processo=saved.numero_processo, metadata={'service_type': saved.service_type, 'status': saved.status.value})
        return saved

    async def conclude_record(self, record_id: UUID, resumo: str | None=None) -> WorkflowRecord:
        record = await self.repository.get_by_id(record_id)
        if not record:
            raise ValueError('Registo nao encontrado')
        record.concluir(resumo)
        return await self.repository.save(record)

    async def cancel_record(self, record_id: UUID, motivo: str) -> WorkflowRecord:
        record = await self.repository.get_by_id(record_id)
        if not record:
            raise ValueError('Registo nao encontrado')
        record.cancelar(motivo)
        return await self.repository.save(record)

    async def get_record(self, record_id: UUID) -> WorkflowRecord | None:
        return await self.repository.get_by_id(record_id)

    async def list_records(self, citizen_id: UUID, service_type: str | None=None) -> list[WorkflowRecord]:
        return await self.repository.list_by_citizen(citizen_id, service_type)