from __future__ import annotations
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.infrastructure.infrastructure.persistence.saga_model import SagaInstanceModel
from apps.backend.app.modules.infrastructure.infrastructure.persistence.saga_repository import SQLAlchemySagaRepository

class ExecucaoObraStates:
    INICIADA = 'INICIADA'
    EMPENHO_GERADO = 'EMPENHO_GERADO'
    TCU_NOTIFICADO = 'TCU_NOTIFICADO'
    FINALIZADA = 'FINALIZADA'
    FALHA = 'FALHA'

@dataclass(frozen=True)
class SagaTransitionResult:
    saga_state: str
    completed: bool

class ExecucaoObraSaga:
    SAGA_TYPE = 'ExecucaoObra'

    def __init__(self, saga_repo: SQLAlchemySagaRepository) -> None:
        self._saga_repo = saga_repo

    async def advance(self, session: AsyncSession, *, event_type: str, payload: dict, correlation_id: str, tenant_id: str) -> SagaTransitionResult:
        saga = await self._saga_repo.get_by_correlation(session, saga_type=self.SAGA_TYPE, correlation_id=correlation_id, tenant_id=tenant_id)
        if saga is None:
            saga = await self._saga_repo.create_if_absent(session, saga_type=self.SAGA_TYPE, correlation_id=correlation_id, tenant_id=tenant_id, state=ExecucaoObraStates.INICIADA, data={'obra_id': payload.get('obra_id'), 'last_event_type': event_type})
        next_state = self._next_state(event_type=event_type, current_state=saga.state)
        merged_data = dict(saga.data or {})
        merged_data.update({'obra_id': payload.get('obra_id', merged_data.get('obra_id')), 'codigo_obra': payload.get('codigo_obra', merged_data.get('codigo_obra')), 'last_event_type': event_type})
        completed = next_state == ExecucaoObraStates.FINALIZADA
        await self._saga_repo.update_state(session, row=saga, state=next_state, data=merged_data, completed=completed)
        return SagaTransitionResult(saga_state=next_state, completed=completed)

    async def mark_failed(self, session: AsyncSession, *, correlation_id: str, tenant_id: str, reason: str) -> None:
        saga = await self._saga_repo.get_by_correlation(session, saga_type=self.SAGA_TYPE, correlation_id=correlation_id, tenant_id=tenant_id)
        if saga is None:
            saga = await self._saga_repo.create_if_absent(session, saga_type=self.SAGA_TYPE, correlation_id=correlation_id, tenant_id=tenant_id, state=ExecucaoObraStates.FALHA, data={'error': reason})
            return
        data = dict(saga.data or {})
        data['error'] = reason
        await self._saga_repo.update_state(session, row=saga, state=ExecucaoObraStates.FALHA, data=data, completed=False)

    def _next_state(self, *, event_type: str, current_state: str) -> str:
        if event_type == 'ObraIniciadaEvent':
            return ExecucaoObraStates.INICIADA
        if event_type == 'MedicaoAprovadaEvent':
            return ExecucaoObraStates.EMPENHO_GERADO
        if event_type == 'AditivoAssinadoEvent':
            return ExecucaoObraStates.TCU_NOTIFICADO
        if event_type == 'ObraConcluidaEvent':
            return ExecucaoObraStates.FINALIZADA
        return current_state
