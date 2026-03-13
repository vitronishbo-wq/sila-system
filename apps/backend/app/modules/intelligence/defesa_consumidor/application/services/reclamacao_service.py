from __future__ import annotations
import uuid
from datetime import datetime
from typing import Any
from apps.backend.app.domain.events import get_event_bus
from apps.backend.app.modules.intelligence.defesa_consumidor.application.ports.reclamacao_repository_port import ReclamacaoRepositoryPort
from apps.backend.app.modules.intelligence.defesa_consumidor.domain.exceptions import ReclamacaoJaEncerradaException, ReclamacaoNaoEncontradaException

class ReclamacaoService:

    def __init__(self, repository: ReclamacaoRepositoryPort, event_bus: Any | None=None):
        self.repository = repository
        self.event_bus = event_bus or get_event_bus()

    async def criar_reclamacao(self, data: dict[str, Any]) -> dict[str, Any]:
        if not data.get('consumidor_id') or not data.get('estabelecimento_id'):
            raise ValueError('consumidor_id e estabelecimento_id sao obrigatorios')
        payload = dict(data)
        payload['protocolo'] = self._gerar_protocolo()
        payload['status'] = (payload.get('status') or 'aberta').lower()
        payload['prioridade'] = (payload.get('prioridade') or 'media').lower()
        reclamacao = await self.repository.create(payload)
        await self.event_bus.publish('defesa_consumidor.reclamacao.criada', {'id': reclamacao.get('id'), 'protocolo': reclamacao.get('protocolo'), 'consumidor_id': reclamacao.get('consumidor_id'), 'estabelecimento_id': reclamacao.get('estabelecimento_id'), 'categoria': reclamacao.get('categoria'), 'data_abertura': self._iso(reclamacao.get('data_abertura'))})
        return reclamacao

    async def obter_reclamacao(self, reclamacao_id: int) -> dict[str, Any]:
        reclamacao = await self.repository.get_by_id(reclamacao_id)
        if not reclamacao:
            raise ReclamacaoNaoEncontradaException(reclamacao_id)
        return reclamacao

    async def atualizar_status(self, reclamacao_id: int, novo_status: str) -> dict[str, Any]:
        reclamacao = await self.obter_reclamacao(reclamacao_id)
        if reclamacao.get('resolvido'):
            raise ReclamacaoJaEncerradaException(reclamacao_id)
        status_antigo = reclamacao.get('status')
        reclamacao['status'] = novo_status.lower()
        updated = await self.repository.update(reclamacao)
        await self.event_bus.publish('defesa_consumidor.reclamacao.status_atualizado', {'id': reclamacao_id, 'protocolo': reclamacao.get('protocolo'), 'status_anterior': status_antigo, 'status_novo': updated.get('status'), 'data_atualizacao': datetime.utcnow().isoformat()})
        return updated

    async def finalizar_reclamacao(self, reclamacao_id: int, resolvido: bool=True, descricao_resposta: str | None=None) -> dict[str, Any]:
        reclamacao = await self.obter_reclamacao(reclamacao_id)
        if reclamacao.get('resolvido'):
            raise ReclamacaoJaEncerradaException(reclamacao_id)
        data_resolucao = datetime.utcnow()
        data_abertura = reclamacao.get('data_abertura') or data_resolucao
        if isinstance(data_abertura, str):
            data_abertura = datetime.fromisoformat(data_abertura)
        dias_aberto = max((data_resolucao - data_abertura).days, 0)
        reclamacao['resolvido'] = resolvido
        reclamacao['status'] = 'encerrada'
        reclamacao['data_resolucao'] = data_resolucao
        reclamacao['descricao_resposta'] = descricao_resposta
        updated = await self.repository.update(reclamacao)
        await self.event_bus.publish('defesa_consumidor.reclamacao.finalizada', {'id': reclamacao_id, 'protocolo': reclamacao.get('protocolo'), 'resolvido': resolvido, 'dias_resolucao': dias_aberto, 'data_resolucao': data_resolucao.isoformat()})
        return updated

    async def escalar_prioridade(self, reclamacao_id: int) -> dict[str, Any]:
        reclamacao = await self.obter_reclamacao(reclamacao_id)
        ordem = ['baixa', 'media', 'alta', 'critica']
        atual = (reclamacao.get('prioridade') or 'media').lower()
        try:
            idx = ordem.index(atual)
        except ValueError:
            idx = 1
        if idx >= len(ordem) - 1:
            return reclamacao
        nova = ordem[idx + 1]
        reclamacao['prioridade'] = nova
        updated = await self.repository.update(reclamacao)
        await self.event_bus.publish('defesa_consumidor.reclamacao.prioridade_escalada', {'id': reclamacao_id, 'protocolo': reclamacao.get('protocolo'), 'prioridade_anterior': atual, 'prioridade_nova': nova})
        return updated

    async def listar_por_consumidor(self, consumidor_id: int, limit: int=50) -> list[dict[str, Any]]:
        return await self.repository.list_by_consumidor(consumidor_id, limit)

    async def listar_prioritarias(self, prioridade: str='alta', limit: int=50) -> list[dict[str, Any]]:
        return await self.repository.list_prioritarias(prioridade.lower(), limit)

    def _gerar_protocolo(self) -> str:
        return f'DC-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}'

    @staticmethod
    def _iso(value: Any) -> Any:
        if isinstance(value, datetime):
            return value.isoformat()
        return value