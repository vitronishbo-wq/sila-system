from __future__ import annotations
from uuid import UUID
from app.modules.infrastructure.infrastructure.adapters.service_requests_service_adapter import ServiceRequestsServiceAdapter
from app.modules.infrastructure.infrastructure.adapters.workflow_service_adapter import WorkflowServiceAdapter

async def handle_criacao(payload: dict, tenant_id: str, correlation_id: str) -> None:
    service_requests = ServiceRequestsServiceAdapter()
    workflow = WorkflowServiceAdapter()
    await service_requests.abrir_solicitacao({'tipo': 'obra_publica', 'codigo_obra': payload.get('codigo_obra'), 'municipio': payload.get('municipio'), 'provincia': payload.get('provincia'), 'tenant_id': tenant_id, 'correlation_id': correlation_id})
    await workflow.iniciar_fluxo(entidade='obras_publicas_obra', referencia_id=UUID(str(payload['obra_id'])), contexto={'codigo_obra': payload.get('codigo_obra'), 'tenant_id': tenant_id, 'correlation_id': correlation_id})

async def handle_inicio(payload: dict, tenant_id: str, correlation_id: str) -> None:
    workflow = WorkflowServiceAdapter()
    await workflow.registrar_evento(workflow_id=payload.get('codigo_obra', 'OBRA'), evento='obra_em_execucao', payload={**payload, '_tenant_id': tenant_id, '_correlation_id': correlation_id})

async def handle_conclusao(payload: dict, tenant_id: str, correlation_id: str) -> None:
    workflow = WorkflowServiceAdapter()
    await workflow.registrar_evento(workflow_id=payload.get('codigo_obra', 'OBRA'), evento='obra_concluida', payload={**payload, '_tenant_id': tenant_id, '_correlation_id': correlation_id})
