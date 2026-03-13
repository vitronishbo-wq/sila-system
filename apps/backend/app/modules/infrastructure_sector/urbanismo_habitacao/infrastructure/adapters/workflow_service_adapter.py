from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.workflow_service_port import WorkflowServicePort

class WorkflowServiceAdapter(WorkflowServicePort):

    async def iniciar_fluxo(self, *, entidade: str, referencia_id: UUID, contexto: dict) -> str:
        _ = (entidade, referencia_id, contexto)
        return f'WF-{str(referencia_id)[:8].upper()}'

    async def registrar_evento(self, *, workflow_id: str, evento: str, payload: dict) -> None:
        _ = (workflow_id, evento, payload)