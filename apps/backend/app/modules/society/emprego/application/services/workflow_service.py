from __future__ import annotations
from datetime import date
from typing import Optional
from uuid import UUID, uuid4
from apps.backend.app.modules.society.emprego.application.ports import CitizenServicePort, RequestServicePort, WorkflowRepositoryPort
from apps.backend.app.modules.society.emprego.domain.models._workflow_record import WorkflowEmpregoRecord

class WorkflowService:

    def __init__(self, *, repository: WorkflowRepositoryPort, process_prefix: str, citizen_service: CitizenServicePort | None=None, request_service: RequestServicePort | None=None):
        self.repository = repository
        self.process_prefix = process_prefix
        self.citizen_service = citizen_service
        self.request_service = request_service

    async def criar_registro(self, *, service_type: str, citizen_id: UUID, observacoes: Optional[str]=None, metadata: Optional[dict]=None) -> WorkflowEmpregoRecord:
        if self.citizen_service is not None:
            active = await self.citizen_service.is_citizen_active(citizen_id)
            if not active:
                raise ValueError(f'Cidadao {citizen_id} nao encontrado ou inativo')
        exists = await self.repository.exists_active_for_citizen(citizen_id, service_type)
        if exists:
            raise ValueError('Cidadao ja possui registro ativo para este servico')
        numero = await self.repository.next_numero_processo(date.today().year, self.process_prefix)
        item = WorkflowEmpregoRecord(id=uuid4(), numero_processo=numero, citizen_id=citizen_id, data_registro=date.today(), service_type=service_type, observacoes=observacoes, metadata=metadata or {})
        saved = await self.repository.save(item)
        if self.request_service is not None:
            await self.request_service.create_request(request_type=service_type, entity_id=saved.id, citizen_id=saved.citizen_id, numero_processo=saved.numero_processo, metadata=saved.metadata)
        return saved

    async def concluir_registro(self, *, item_id: UUID, actor_id: UUID, observacoes: Optional[str]=None) -> WorkflowEmpregoRecord:
        item = await self.repository.get_by_id(item_id)
        if not item:
            raise ValueError('Registro nao encontrado')
        item.concluir(observacoes)
        updated = await self.repository.save(item)
        if self.request_service is not None:
            await self.request_service.complete_request(entity_id=item_id, actor_id=actor_id, metadata={'service_type': updated.service_type, 'status': updated.status.value})
        return updated

    async def cancelar_registro(self, *, item_id: UUID, actor_id: UUID, motivo: str) -> WorkflowEmpregoRecord:
        item = await self.repository.get_by_id(item_id)
        if not item:
            raise ValueError('Registro nao encontrado')
        item.cancelar(motivo)
        updated = await self.repository.save(item)
        if self.request_service is not None:
            await self.request_service.complete_request(entity_id=item_id, actor_id=actor_id, metadata={'service_type': updated.service_type, 'status': updated.status.value, 'motivo': motivo})
        return updated

    async def obter_por_id(self, item_id: UUID) -> WorkflowEmpregoRecord | None:
        return await self.repository.get_by_id(item_id)

    async def listar_por_cidadao(self, citizen_id: UUID, service_type: str | None=None) -> list[WorkflowEmpregoRecord]:
        return await self.repository.list_by_citizen(citizen_id, service_type)